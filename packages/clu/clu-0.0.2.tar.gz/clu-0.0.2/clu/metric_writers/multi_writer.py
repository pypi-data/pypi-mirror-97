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

"""MetricWriter that writes to multiple MetricWriters."""

from typing import Any, Mapping, Optional, Sequence

from clu.metric_writers import interface
import numpy as np

Scalar = interface.Scalar


class MultiWriter(interface.MetricWriter):
  """MetricWriter that writes to multiple writers at once."""

  def __init__(self, writers: Sequence[interface.MetricWriter]):
    self._writers = tuple(writers)

  def write_scalars(self, step: int, scalars: Mapping[str, Scalar]):
    for w in self._writers:
      w.write_scalars(step, scalars)

  def write_images(self, step: int, images: Mapping[str, np.ndarray]):
    for w in self._writers:
      w.write_images(step, images)

  def write_texts(self, step: int, texts: Mapping[str, str]):
    for w in self._writers:
      w.write_texts(step, texts)

  def write_histograms(self,
                       step: int,
                       arrays: Mapping[str, np.ndarray],
                       num_buckets: Optional[Mapping[str, int]] = None):
    for w in self._writers:
      w.write_histograms(step, arrays, num_buckets)

  def write_hparams(self, hparams: Mapping[str, Any]):
    for w in self._writers:
      w.write_hparams(hparams)

  def flush(self):
    for w in self._writers:
      w.flush()

  def close(self):
    for w in self._writers:
      w.close()
