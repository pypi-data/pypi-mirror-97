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

"""Tests for parameter overviews."""

from clu import parameter_overview
from flax import linen as nn
import jax
import jax.numpy as jnp
import sonnet as snt
import tensorflow as tf

EMPTY_PARAMETER_OVERVIEW = """+------+-------+------+------+-----+
| Name | Shape | Size | Mean | Std |
+------+-------+------+------+-----+
+------+-------+------+------+-----+
Total: 0"""

SNT_CONV2D_PARAMETER_OVERVIEW = """+----------+--------------+------+
| Name     | Shape        | Size |
+----------+--------------+------+
| conv/b:0 | (2,)         | 2    |
| conv/w:0 | (3, 3, 3, 2) | 54   |
+----------+--------------+------+
Total: 56"""

SNT_CONV2D_PARAMETER_OVERVIEW_WITH_STATS = """+----------+--------------+------+---------+-------+
| Name     | Shape        | Size | Mean    | Std   |
+----------+--------------+------+---------+-------+
| conv/b:0 | (2,)         | 2    | 0.0     | 0.0   |
| conv/w:0 | (3, 3, 3, 2) | 54   | -0.0127 | 0.157 |
+----------+--------------+------+---------+-------+
Total: 56"""

FLAX_CONV2D_PARAMETER_OVERVIEW = """+-------------+--------------+------+
| Name        | Shape        | Size |
+-------------+--------------+------+
| conv/bias   | (2,)         | 2    |
| conv/kernel | (3, 3, 3, 2) | 54   |
+-------------+--------------+------+
Total: 56"""

FLAX_CONV2D_PARAMETER_OVERVIEW_WITH_STATS = """+-------------+--------------+------+--------+-------+
| Name        | Shape        | Size | Mean   | Std   |
+-------------+--------------+------+--------+-------+
| conv/bias   | (2,)         | 2    | 0.0    | 0.0   |
| conv/kernel | (3, 3, 3, 2) | 54   | 0.0562 | 0.188 |
+-------------+--------------+------+--------+-------+
Total: 56"""

FLAX_CONV2D_MAPPING_PARAMETER_OVERVIEW_WITH_STATS = """+--------------------+--------------+------+--------+-------+
| Name               | Shape        | Size | Mean   | Std   |
+--------------------+--------------+------+--------+-------+
| params/conv/bias   | (2,)         | 2    | 0.0    | 0.0   |
| params/conv/kernel | (3, 3, 3, 2) | 54   | 0.0562 | 0.188 |
+--------------------+--------------+------+--------+-------+
Total: 56"""


class TfParameterOverviewTest(tf.test.TestCase):

  def test_count_parameters_empty(self):
    module = snt.Module()
    snt.allow_empty_variables(module)

    # No variables.
    self.assertEqual(0, parameter_overview.count_parameters(module))

    # Single variable.
    module.var = tf.Variable([0, 1])
    self.assertEqual(2, parameter_overview.count_parameters(module))

  def test_count_parameters_on_module(self):
    module = snt.Module()
    # Weights of a 2D convolution with 2 filters..
    module.conv = snt.Conv2D(output_channels=2, kernel_shape=3, name="conv")
    module.conv(tf.ones((2, 5, 5, 3)))  # 3 * 3*3 * 2 + 2 (bias) = 56 parameters
    self.assertEqual(56, parameter_overview.count_parameters(module))

  def test_count_parameters_on_module_with_duplicate_names(self):
    module = snt.Module()
    # Weights of a 2D convolution with 2 filters..
    module.conv = snt.Conv2D(output_channels=2, kernel_shape=3, name="conv")
    module.conv(tf.ones((2, 5, 5, 3)))  # 3 * 3*3 * 2 + 2 (bias) = 56 parameters
    module.conv2 = snt.Conv2D(output_channels=2, kernel_shape=3, name="conv")
    module.conv2(tf.ones(
        (2, 5, 5, 3)))  # 3 * 3*3 * 2 + 2 (bias) = 56 parameters
    parameter_overview.log_parameter_overview(module)
    self.assertEqual(112, parameter_overview.count_parameters(module))

  def test_get_parameter_overview_empty(self):
    module = snt.Module()
    snt.allow_empty_variables(module)

    # No variables.
    self.assertEqual(EMPTY_PARAMETER_OVERVIEW,
                     parameter_overview.get_parameter_overview(module))

    module.conv = snt.Conv2D(output_channels=2, kernel_shape=3)
    # Variables not yet created (happens in the first forward pass).
    self.assertEqual(EMPTY_PARAMETER_OVERVIEW,
                     parameter_overview.get_parameter_overview(module))

  def test_get_parameter_overview_on_module(self):
    module = snt.Module()
    # Weights of a 2D convolution with 2 filters..
    module.conv = snt.Conv2D(output_channels=2, kernel_shape=3, name="conv")
    module.conv(tf.ones((2, 5, 5, 3)))  # 3 * 3^2 * 2 = 56 parameters
    self.assertEqual(
        SNT_CONV2D_PARAMETER_OVERVIEW,
        parameter_overview.get_parameter_overview(module, include_stats=False))
    self.assertEqual(SNT_CONV2D_PARAMETER_OVERVIEW_WITH_STATS,
                     parameter_overview.get_parameter_overview(module))


class CNN(nn.Module):

  @nn.compact
  def __call__(self, x):
    return nn.Conv(features=2, kernel_size=(3, 3), name="conv")(x)


class JaxParameterOverviewTest(tf.test.TestCase):

  def test_count_parameters_empty(self):
    self.assertEqual(0, parameter_overview.count_parameters({}))

  def test_count_parameters(self):
    rng = jax.random.PRNGKey(42)
    # Weights of a 2D convolution with 2 filters..
    variables = CNN().init(rng, jnp.zeros((2, 5, 5, 3)))
    # 3 * 3*3 * 2 + 2 (bias) = 56 parameters
    self.assertEqual(56,
                     parameter_overview.count_parameters(variables["params"]))

  def test_get_parameter_overview_empty(self):
    self.assertEqual(EMPTY_PARAMETER_OVERVIEW,
                     parameter_overview.get_parameter_overview({}))

  def test_get_parameter_overview(self):
    rng = jax.random.PRNGKey(42)
    # Weights of a 2D convolution with 2 filters..
    variables = CNN().init(rng, jnp.zeros((2, 5, 5, 3)))
    self.assertEqual(
        FLAX_CONV2D_PARAMETER_OVERVIEW,
        parameter_overview.get_parameter_overview(
            variables["params"], include_stats=False))
    print(parameter_overview.get_parameter_overview(variables["params"]))
    self.assertEqual(
        FLAX_CONV2D_PARAMETER_OVERVIEW_WITH_STATS,
        parameter_overview.get_parameter_overview(variables["params"]))
    print(parameter_overview.get_parameter_overview(variables))
    self.assertEqual(
        FLAX_CONV2D_MAPPING_PARAMETER_OVERVIEW_WITH_STATS,
        parameter_overview.get_parameter_overview(variables))


if __name__ == "__main__":
  tf.test.main()
