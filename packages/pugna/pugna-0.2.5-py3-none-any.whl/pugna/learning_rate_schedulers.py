"""
New learning rate scheduler classes
that inherit from LearningRateSchedule.

See https://github.com/tensorflow/tensorflow/blob/v2.2.0/tensorflow/python/keras/optimizer_v2/learning_rate_schedule.py

"""

import abc
import math

from tensorflow.python.framework import constant_op
from tensorflow.python.framework import ops
from tensorflow.python.ops import math_ops
from tensorflow.python.util.tf_export import keras_export
from tensorflow.keras.optimizers.schedules import LearningRateSchedule


@keras_export("keras.optimizers.schedules.InverseTimeDecay_WithFinalLR")
class InverseTimeDecay_WithFinalLR(LearningRateSchedule):
    """This is based on InverseTimeDecay but includes a 'final_learning_rate'
    parameter."""

    def __init__(
            self,
            initial_learning_rate,
            final_learning_rate,
            decay_steps,
            decay_rate,
            staircase=False,
            name=None):
        """Applies inverse time decay to the initial learning rate.
        When training a model, it is often recommended to lower the learning rate as
        the training progresses. This schedule applies the inverse decay function
        to an optimizer step, given a provided initial learning rate.
        It requires a `step` value to compute the decayed learning rate. You can
        just pass a TensorFlow variable that you increment at each training step.
        The schedule a 1-arg callable that produces a decayed learning
        rate when passed the current optimizer step. This can be useful for changing
        the learning rate value across different invocations of optimizer functions.
        It is computed as:
        ```python
        def decayed_learning_rate(step):
          return (initial_learning_rate-final_learning_rate) / (1 + decay_rate * step / decay_step) + final_learning_rate
        ```
        or, if `staircase` is `True`, as:
        ```python
        def decayed_learning_rate(step):
          return (initial_learning_rate-final_learning_rate) / (1 + decay_rate * floor(step / decay_steps)) + final_learning_rate
        ```
        You can pass this schedule directly into a `tf.keras.optimizers.Optimizer`
        as the learning rate.
        Example: Fit a Keras model when decaying 1/t with a rate of 0.5:
        ```python
        ...
        initial_learning_rate = 0.1
        final_learning_rate = 1e-5
        decay_steps = 1.0
        decay_rate = 0.5
        learning_rate_fn = keras.optimizers.schedules.InverseTimeDecay_WithFinalLR(
          initial_learning_rate, final_learning_rate, decay_steps, decay_rate)
        model.compile(optimizer=tf.keras.optimizers.SGD(
                          learning_rate=learning_rate_fn),
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(data, labels, epochs=5)
        ```
        Args:
          initial_learning_rate: A scalar `float32` or `float64` `Tensor` or a
            Python number.  The initial learning rate.
          final_learning_rate: A scalar `float32` or `float64` `Tensor` or a
            Python number.  The final learning rate.
          decay_steps: How often to apply decay.
          decay_rate: A Python number.  The decay rate.
          staircase: Whether to apply decay in a discrete staircase, as opposed to
            continuous, fashion.
          name: String.  Optional name of the operation.  Defaults to
            'InverseTimeDecay_WithFinalLR'.
        Returns:
          A 1-arg callable learning rate schedule that takes the current optimizer
          step and outputs the decayed learning rate, a scalar `Tensor` of the same
          type as `initial_learning_rate`.
        """
        super(InverseTimeDecay_WithFinalLR, self).__init__()

        self.initial_learning_rate = initial_learning_rate
        self.final_learning_rate = final_learning_rate
        self.decay_steps = decay_steps
        self.decay_rate = decay_rate
        self.staircase = staircase
        self.name = name

    def __call__(self, step):
        with ops.name_scope_v2(self.name or "InverseTimeDecay_WithFinalLR") as name:
            initial_learning_rate = ops.convert_to_tensor_v2(
                self.initial_learning_rate, name="initial_learning_rate")
            final_learning_rate = ops.convert_to_tensor_v2(
                self.final_learning_rate, name="final_learning_rate")
            dtype = initial_learning_rate.dtype
            decay_steps = math_ops.cast(self.decay_steps, dtype)
            decay_rate = math_ops.cast(self.decay_rate, dtype)

            global_step_recomp = math_ops.cast(step, dtype)
            p = global_step_recomp / decay_steps
            if self.staircase:
                p = math_ops.floor(p)
            const = math_ops.cast(constant_op.constant(1), dtype)
            denom = math_ops.add(const, math_ops.multiply(decay_rate, p))
            numerator = math_ops.subtract(
                initial_learning_rate, final_learning_rate)
            fraction = math_ops.divide(numerator, denom)
            return math_ops.add(fraction, final_learning_rate, name=name)

    def get_config(self):
        return {
            "initial_learning_rate": self.initial_learning_rate,
            "final_learning_rate": self.final_learning_rate,
            "decay_steps": self.decay_steps,
            "decay_rate": self.decay_rate,
            "staircase": self.staircase,
            "name": self.name
        }
