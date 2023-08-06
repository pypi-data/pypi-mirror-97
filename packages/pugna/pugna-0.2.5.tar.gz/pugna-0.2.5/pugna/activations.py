"""custom activation functions
"""
import numpy as np
import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.keras import layers
from tensorflow.python.keras.utils import tf_utils

# custom layer code based on help
# from https://keras.io/examples/keras_recipes/antirectifier/


class sReLU_Layer(layers.Layer):
    """The sReLU activation function is defined on page 4 of 1910.11710.
    It is a Compact supported activation function.

    sReLU(x) = ReLU(−(x − 1)) × ReLU(x)
    """

    def __init__(self, **kwargs):
        super(sReLU_Layer, self).__init__(**kwargs)

    def call(self, inputs):
        return K.relu(-(inputs-1)) * K.relu(inputs)

    def get_config(self):
        base_config = super(sReLU_Layer, self).get_config()
        return dict(list(base_config.items()))

    @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return input_shape


class sReLU_2_Layer(layers.Layer):
    """Compact supported activation function.
    The sReLU activation function raised to the power of 2.
    This makes the activation function have a smooth derivative

    sReLU_2(x) = sReLU(x)**2
    """

    def __init__(self, **kwargs):
        super(sReLU_2_Layer, self).__init__(**kwargs)

    def call(self, inputs):
        return tf.math.pow(K.relu(-(inputs-1)) * K.relu(inputs), 2)

    def get_config(self):
        base_config = super(sReLU_2_Layer, self).get_config()
        return dict(list(base_config.items()))

    @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return input_shape


class sReLU_3_Layer(layers.Layer):
    """Compact supported activation function.
    The sReLU activation function raised to the power of 3.
    This makes the activation function have a smooth derivative

    sReLU_3(x) = sReLU(x)**3
    """

    def __init__(self, **kwargs):
        super(sReLU_3_Layer, self).__init__(**kwargs)

    def call(self, inputs):
        return tf.math.pow(K.relu(-(inputs-1)) * K.relu(inputs), 3)

    def get_config(self):
        base_config = super(sReLU_3_Layer, self).get_config()
        return dict(list(base_config.items()))

    @tf_utils.shape_type_conversion
    def compute_output_shape(self, input_shape):
        return input_shape


def sReLU(x):
    """
    page 4 of 1910.11710
    """
    return tf.nn.relu(-(x-1)) * tf.nn.relu(x)


def sReLU2(x):
    return sReLU(x)**2


def sReLU3(x):
    return sReLU(x)**3


def sReLUn(x, n):
    """
    generalisation of sReLU. Raises sReLU to the power n.
    """
    return sReLU(x)**n


def s2relu(x):
    """presented in 2009.14597

    Args:
        x ([type]): [description]

    Returns:
        [type]: [description]
    """
    return tf.sin(2*np.pi*x)*sReLU(x)
