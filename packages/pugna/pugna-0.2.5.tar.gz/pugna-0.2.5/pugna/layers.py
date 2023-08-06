import tensorflow as tf
from tensorflow.keras.layers import Layer


@tf.function(autograph=True)
def tf_compute_K(n_neurons, n_parts):
    """equation 18 from 1910.11710

    a_i = i
    """
    K = tf.ones(1, dtype=tf.float32)
    j = 0
    ratio = tf.cast(n_neurons/n_parts, tf.int32)
    for i in tf.range(n_neurons):
        tf.autograph.experimental.set_loop_options(
            shape_invariants=[(K, tf.TensorShape([None]))])
        if tf.cast(tf.math.mod(i, ratio), tf.int32) == 0:
            j = j + 1
        if i != 0:
            K = tf.concat([K, [j]], axis=0)
    return K


@tf.function(autograph=True)
def tf_compute_K_power2(n_neurons, n_parts):
    """https://arxiv.org/abs/2007.11207
    below equation 3.5

    a_i = 2**(i-1)
    """
    K = tf.ones(1, dtype=tf.float32)
    j = 0
    ratio = tf.cast(n_neurons/n_parts, tf.int32)
    for i in tf.range(n_neurons):
        tf.autograph.experimental.set_loop_options(
            shape_invariants=[(K, tf.TensorShape([None]))])
        if tf.cast(tf.math.mod(i, ratio), tf.int32) == 0:
            j = j + 1
        if i != 0:
            K = tf.concat([K, [2**(j-1)]], axis=0)
    return K


class Mscale(Layer):
    """
    implementing MscaleDNN
    https://arxiv.org/pdf/1910.11710.pdf
    https://arxiv.org/pdf/2007.11207v1.pdf
    https://arxiv.org/pdf/2009.14597.pdf
    https://github.com/xuzhiqin1990/mscalednn/blob/main/code/my_act.py
    """

    def __init__(self, units=32, Nscales=1, scale_name="linear", name=None, **kwargs):
        """

        Args:
            units (int, optional): number of units per feature. Defaults to 32.
            Nscales (int, optional): number of scales. Defaults to 1.
            scale_name (str, optional): scale type choices: ["linear", "base2"]
        """
        super(Mscale, self).__init__(name=name)
        self.units = units
        self.Nscales = Nscales
        self.scale_name = scale_name
        super(Mscale, self).__init__(**kwargs)

    def build(self, input_shape):
        self.w = self.add_weight(shape=(
            input_shape[-1], self.units), initializer="random_normal",
            trainable=True, name="w")

        self.b = self.add_weight(
            shape=(self.units,), initializer="random_normal", trainable=True,
            name="b")

        if self.scale_name == 'linear':
            self.K = tf_compute_K(self.units, self.Nscales)
        elif self.scale_name == 'base2':
            self.K = tf_compute_K_power2(self.units, self.Nscales)

    def call(self, inputs):
        scaled = tf.math.multiply(self.K, self.w)
        return tf.matmul(inputs, scaled) + self.b

    def get_config(self):
        config = super(Mscale, self).get_config()
        config.update({"units": self.units, "Nscales": self.Nscales})
        return config


def relu_n(x, n=1):
    """ReLU activation clipped at n.
    got this from 2004.13912"""
    return tf.clip_by_value(x, 0, n)


class ExU(Layer):
    """Exponential centred from NAMs paper 2004.13912
    But generalised to handle multiple input features
    """

    def __init__(self, units):
        super(ExU, self).__init__()
        self.units = units
        self._w_initializer = tf.initializers.TruncatedNormal(
            mean=4.0, stddev=0.5)

    def build(self, input_shape):
        # input_shape[-1] is the number of features
        self.w = self.add_weight(
            name="w",
            shape=(input_shape[-1], self.units),
            initializer=self._w_initializer,
            trainable=True
        )
        self.b = self.add_weight(
            name="b",
            shape=(1, self.units),
            initializer=tf.initializers.TruncatedNormal(stddev=0.5),
            trainable=True
        )

    @tf.function
    def call(self, inputs):

        # this is a outer subtraction
        c_pij = tf.transpose(inputs, perm=[0, 1])[..., tf.newaxis] - self.b
        h = tf.reduce_sum(c_pij * tf.math.exp(self.w), axis=1)

        return relu_n(h)
