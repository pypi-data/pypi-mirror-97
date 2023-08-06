# Copyright 2021 The CLU Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""PeriodicActions execute small actions periodically in the training loop."""

import abc
import collections
import concurrent.futures
import contextlib
import queue
import sys
import time
from typing import Callable, Optional, Sequence

from absl import logging
from clu import metric_writers
from clu import platform
from clu import profiler

import jax
import jax.numpy as jnp
import wrapt



MetricWriter = metric_writers.MetricWriter


def _make_async(thread_name_prefix=""):
  """Returns a decorator that runs any function it wraps in a background thread.

   When called, the decorated function will immediately return a future
   representing its result.
   The function being decorated can be an instance method or normal function.
   Consecutive calls to the decorated function are guaranteed to be in order
   and non overlapping.
   An error raised by the decorated function will be raised in the background
   thread at call-time. Raising the error in the main thread is deferred until
   the next call, so as to be non-blocking.
   All subsequent calls to the decorated function after an error has been
   raised
   will not run (regardless of whether the arguments have changed); instead
   they will re-raise the original error in the main thread.

  Args:
    thread_name_prefix: Str prefix for the background thread, for easier
      debugging.

  Returns:
    decorator that runs any function it wraps in a background thread, and
    handles any errors raised.
  """
  # We have a single thread pool per wrapped function to ensure that calls to
  # the function are run in order (but in a background thread).
  pool = concurrent.futures.ThreadPoolExecutor(
      max_workers=1, thread_name_prefix=thread_name_prefix)
  errors = []

  @wrapt.decorator
  def decorator(wrapped, instance, args, kwargs):
    """Runs wrapped in a background thread so result is non-blocking.

    Args:
      wrapped: A function to wrap and execute in background thread. Can be
        instance method or normal function.
      instance: The object to which the wrapped function was bound when it was
        called (None if wrapped is a normal function).
      args: List of position arguments supplied when wrapped function was
        called.
      kwargs: Dict of keyword arguments supplied when the wrapped function was
        called.

    Returns:
      A future representing the result of calling wrapped.
    Raises:
      Exception object caught in background thread, if call to wrapped fails.
      Exception object with stacktrace in main thread, if the previous call to
        wrapped failed.
    """

    def trap_errors(*args, **kwargs):
      """Wraps wrapped to trap any errors thrown."""

      if errors:
        # Do not execute wrapped if previous call errored.
        return
      try:
        return wrapped(*args, **kwargs)
      except Exception as e:
        errors.append(sys.exc_info())
        logging.exception("Error in producer thread for %s", thread_name_prefix)
        raise e

    if errors:
      # Previous call had an error, re-raise in main thread.
      exc_info = errors[-1]
      raise exc_info[1].with_traceback(exc_info[2])
    del instance
    return pool.submit(trap_errors, *args, **kwargs)

  return decorator


@jax.jit
def _squareit(x):
  """Minimalistic function for use in _wait_jax_async_dispatch()."""
  return x**2


def _wait_jax_async_dispatch():
  """Creates a simple JAX program and waits for its completion.

  Since JAX operations are put in a queue and dispatched one after the other,
  all previously enqueued computations will be finished after a call to this
  function.
  """
  _squareit(jnp.array(0.)).block_until_ready()


class PeriodicAction(abc.ABC):
  """Abstract base class for perodic actions.

  The idea is that the user creates periodic actions and calls them after
  each training step. The base class will trigger in fixed step/time interval
  but subclasses can overwrite `_should_trigger()` to change this behavior.
  Subclasses must implement `_apply()` to perform the action.
  """

  def __init__(self,
               *,
               every_steps: Optional[int] = None,
               every_secs: Optional[float] = None):
    """Creates an action that triggers periodically.

    Args:
      every_steps: If the current step is divisible by `every_steps`, then an
        action is triggered.
      every_secs: If no action has triggered for specified `every_secs`, then
        an action is triggered. Note that the previous action might have been
        triggered by `every_steps` or by `every_secs`.
    """
    self._every_steps = every_steps
    self._every_secs = every_secs
    # Step and timestamp for the last time the action triggered.
    self._previous_step = None
    self._previous_time = None
    # Just for checking that __call__() was called every step.
    self._last_step = None

  def _init_and_check(self, step: int, t: float) -> bool:
    """Initializes and checks it was called at every step."""
    if self._previous_step is None:
      self._previous_step = step
      self._previous_time = t
      self._last_step = step
      return False
    if self._every_steps is not None and step - self._last_step != 1:
      raise ValueError(f"PeriodicAction must be called after every step once "
                       f"(every_steps={self._every_steps}, "
                       f"previous_step={self._previous_step}, step={step}).")
    self._last_step = step
    return True

  def _should_trigger(self, step: int, t: float) -> bool:
    """Return whether the action should trigger this step."""
    if self._every_steps is not None and step % self._every_steps == 0:
      return True
    if (self._every_secs is not None and
        t - self._previous_time > self._every_secs):
      return True
    return False

  def _after_apply(self, step: int, t: float):
    """Called after each time the action triggered."""
    self._previous_step = step
    self._previous_time = t

  def __call__(self, step: int, t: Optional[float] = None) -> bool:
    """Method to call the hook after every training step.

    Args:
      step: Current step.
      t: Optional timestamp. Will use `time.time()` if not specified.

    Returns:
      True if the action triggered, False otherwise. Note that the first
      invocation never triggers.
    """
    if t is None:
      t = time.time()

    if self._init_and_check(step, t) and self._should_trigger(step, t):
      self._apply(step, t)
      self._after_apply(step, t)
      return True
    return False

  @abc.abstractmethod
  def _apply(self, step: int, t: float):
    pass


class ReportProgress(PeriodicAction):
  """This hook will set the progress note on the work unit."""

  def __init__(self,
               *,
               num_train_steps: Optional[int] = None,
               writer: Optional[MetricWriter] = None,
               every_steps: Optional[int] = None,
               every_secs: Optional[float] = 60.0):
    """Creates a new ReportProgress hook.

    Warning: The progress and the reported steps_per_sec are estimates. We
    ignore the asynchronous dispatch for JAX and other operations in the
    training loop (e.g. evaluation).

    Args:
      num_train_steps: The total number of training steps for training.
      writer: Optional MetricWriter to report steps_per_sec measurement. This is
        an estimate for precise values use Xprof.
      every_steps: How often to report the progress in number of training steps.
      every_secs: How often to report progress as time interval.
    """
    super().__init__(every_steps=every_steps, every_secs=every_secs)
    # Check for negative values, e.g. tf.data.UNKNOWN/INFINITE_CARDINALTY.
    if num_train_steps is not None and num_train_steps < 0:
      num_train_steps = None
    self._num_train_steps = num_train_steps
    self._writer = writer
    self._waiting_for_part = collections.defaultdict(queue.Queue)
    self._time_per_part = collections.defaultdict(float)
    self._t0 = time.time()
    # Using max_worker=1 guarantees that the calls to _wait_jax_async_dispatch()
    # happen sequentially.
    self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

  def _should_trigger(self, step: int, t: float):
    # Always trigger at last step.
    return super()._should_trigger(step, t) or step == self._num_train_steps

  def _apply(self, step: int, t: float):
    steps_per_sec = (step - self._previous_step) / (t - self._previous_time)
    message = f"{steps_per_sec:.1f} steps/s"
    if self._num_train_steps:
      eta_seconds = (self._num_train_steps - step) / steps_per_sec
      message += (f", {100 * step / self._num_train_steps:.1f}% @{step}, "
                  f"ETA: {eta_seconds / 60:.0f} min")
    if self._time_per_part:
      total = time.time() - self._t0
      message += " ({:.0f} min : {})".format(total / 60, ", ".join(
          f"{100 * dt / total:.1f}% {name}"
          for name, dt in sorted(self._time_per_part.items())))
    # This should be relatively cheap so we can do it in the same main thread.
    platform.work_unit().set_notes(message)
    if self._writer is not None:
      self._writer.write_scalars(step, {"steps_per_sec": steps_per_sec})

  @contextlib.contextmanager
  def timed(self, name: str, wait_jax_async_dispatch: bool = True):
    # pylint: disable=g-doc-return-or-yield
    """Measures time spent in a named part of the training loop.

    The reported progress will break down the total time into the different
    parts spent inside blocks.

    Example:

      report_progress = hooks.ReportProgress()
      for step, batch in enumerate(train_iter):
        params = train_step(params, batch)
        report_progress(step + 1)
        if (step + 1) % eval_every_steps == 0:
          with report_progress.timed("eval"):
            evaluate()

    The above example would result in the progress being reported as something
    like "10% @1000 ... (5 min : 10% eval)" - assuming that evaluation takes 10%
    of the entire time in this case.

    Args:
      name: Name of the part to be measured.
      wait_jax_async_dispatch: When set to `True`, JAX async dispatch queue will
        be emptied by creating a new computation and waiting for its completion.
        This makes sure that previous computations (e.g. the last train step)
        have actually finished. The same is done before the time is measured.
        Note that this wait happens in a different thread that is only used for
        measuring start/stop time of timed parts. In other words, the measured
        timings reflect the start/stop of the JAX computations within the
        measured part: the timer is started when the last computation before the
        block has finished, and the timer is stopped when the last computation
        from within the block has finished. Note that due to JAX execution these
        operations asynchronously, the measured time might overlap with non-JAX
        computations outside the measured block.
        When set to `False`, then the measured time is of the Python statements
        within the block.
        If there are no expensive JAX computations enqueued in JAX's async
        dispatch queue, then both measurements are identical.
    """
    # pylint: enable=g-doc-return-or-yield
    def start_measurement():
      if wait_jax_async_dispatch:
        _wait_jax_async_dispatch()
      self._waiting_for_part[name].put(time.time())
    self._executor.submit(start_measurement)

    yield

    def stop_measurement():
      if wait_jax_async_dispatch:
        _wait_jax_async_dispatch()
      dt = time.time() - self._waiting_for_part[name].get()
      self._time_per_part[name] += dt
    self._executor.submit(stop_measurement)


class Profile(PeriodicAction):
  """This hook collects calls profiler.start()/stop() every time it triggers.

  """

  def __init__(self,
               *,
               logdir: str,
               num_profile_steps: Optional[int] = 5,
               profile_duration_ms: Optional[int] = 3_000,
               first_profile: int = 10,
               every_steps: Optional[int] = None,
               every_secs: Optional[float] = 3600.0
               ):
    """Initializes a new periodic profiler action.

    Args:
      logdir: Where the profile should be stored (required for
        `tf.profiler.experimental`).
      num_profile_steps: Over how many steps the profile should be taken. Note
        that when specifying both num_profile_steps and profile_duration_ms then
        both conditions will be fulfilled.
      profile_duration_ms: Minimum duration of profile.
      first_profile: First step at which a profile is started.
      every_steps: See `PeriodicAction.__init__()`.
      every_secs: See `PeriodicAction.__init__()`.
    """
    if not num_profile_steps and not profile_duration_ms:
      raise ValueError(
          "Must specify num_profile_steps and/or profile_duration_ms.")
    super().__init__(every_steps=every_steps, every_secs=every_secs)
    self._num_profile_steps = num_profile_steps
    self._first_profile = first_profile
    self._profile_duration_ms = profile_duration_ms
    self._session_running = False
    self._session_started = None
    self._logdir = logdir

  def _should_trigger(self, step: int, t: float) -> bool:
    if self._session_running:
      # If a session is running we only check if we should stop it.
      dt = t - self._session_started
      cond = (not self._profile_duration_ms or
              dt * 1e3 >= self._profile_duration_ms)
      cond &= (not self._num_profile_steps or
               step >= self._previous_step + self._num_profile_steps)
      if cond:
        self._end_session(profiler.stop())
        return False
    # Allow triggering at `self._first_profile` step.
    return super()._should_trigger(step, t) or step == self._first_profile

  def _apply(self, step: int, t: float):
    del step, t  # Unused.
    self._start_session()

  def _start_session(self):
    self._session_running = True
    self._session_started = time.time()
    profiler.start(logdir=self._logdir)

  def _end_session(self, url: Optional[str]):
    platform.work_unit().create_artifact(
        platform.ArtifactType.URL,
        url,
        description=f"[{self._previous_step}] Profile")
    self._session_running = False
    self._session_started = None


class ProfileAllHosts(PeriodicAction):
  """This hook collects calls profiler.collect() every time it triggers.

  """

  def __init__(self,
               *,
               logdir: str,
               hosts: Optional[Sequence[str]] = None,
               profile_duration_ms: int = 3_000,
               first_profile: int = 10,
               every_steps: Optional[int] = None,
               every_secs: Optional[float] = 3600.0):
    """Initializes a new periodic profiler action.

    Args:
      logdir: Where the profile should be stored (required for
        `tf.profiler.experimental`).
      hosts: Addresses of the hosts. If omitted will default to the current job.
      profile_duration_ms: Duration of profile.
      first_profile: First step at which a profile is started.
      every_steps: See `PeriodicAction.__init__()`.
      every_secs: See `PeriodicAction.__init__()`.
    """
    super().__init__(every_steps=every_steps, every_secs=every_secs)
    self._hosts = hosts
    self._first_profile = first_profile
    self._profile_duration_ms = profile_duration_ms
    self._logdir = logdir

  def _should_trigger(self, step: int, t: float) -> bool:
    return super()._should_trigger(step, t) or step == self._first_profile

  def _apply(self, step: int, t: float):
    del step, t  # Unused.
    self._start_session()

  def _start_session(self):
    profiler.collect(
        logdir=self._logdir,
        callback=self._end_session,
        hosts=self._hosts,
        duration_ms=self._profile_duration_ms)

  def _end_session(self, url: Optional[str]):
    platform.work_unit().create_artifact(
        platform.ArtifactType.URL,
        url,
        description=f"[{self._previous_step}] Profile")


class PeriodicCallback(PeriodicAction):
  """This hook calls a callback function each time it triggers."""

  def __init__(self,
               *,
               every_steps: Optional[int] = None,
               every_secs: Optional[float] = None,
               callback_fn: Callable,
               execute_async: bool = False,
               pass_step_and_time: bool = True):
    """Initializes a new periodic Callback action.

    Args:
      every_steps: See `PeriodicAction.__init__()`.
      every_secs: See `PeriodicAction.__init__()`.
      callback_fn: A callback function. It must accept `step` and `t` as
        arguments; arguments are passed by keyword.
      execute_async: if True wraps the callback into an async call.
      pass_step_and_time: if True the step and t are passed to the callback.
    """
    super().__init__(every_steps=every_steps, every_secs=every_secs)
    self._cb_results = collections.deque(maxlen=1)
    self.pass_step_and_time = pass_step_and_time
    if execute_async:
      logging.info("Callback will be executed asynchronously. "
                   "Errors are raised when they become available.")
      self._cb_fn = _make_async(callback_fn.__name__)(callback_fn)  # pylint: disable=no-value-for-parameter
    else:
      self._cb_fn = callback_fn

  def __call__(self, step: int, t: Optional[float] = None, **kwargs) -> bool:
    if t is None:
      t = time.time()

    if self._init_and_check(step, t) and self._should_trigger(step, t):
      # Additional arguments to the callback are passed here through **kwargs.
      self._apply(step, t, **kwargs)
      self._after_apply(step, t)
      return True
    return False

  def get_last_callback_result(self):
    """Returns the last cb result."""
    return self._cb_results[0]

  def _apply(self, step, t, **kwargs):
    if self.pass_step_and_time:
      result = self._cb_fn(step=step, t=t, **kwargs)
    else:
      result = self._cb_fn(**kwargs)
    self._cb_results.append(result)
