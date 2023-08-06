"""
tools to explore effect of hyperparameters
"""

import tensorflow as tf
import pugna.activations


def build_model(input_dim,
                output_dim,
                units_per_layer=128,
                layers_per_block=3,
                n_blocks=3,
                activation='relu',
                leaky_alpha=0.3,
                batch_norm=False,
                summary=True):
    """
    note the way the activation functions are defined.
    This was done because when looking at model.summary()
    if you don't explicitly call the activation function
    i.e. tf.keras.layers.ReLU() or tf.keras.activations.tanh
    **IN** the for loop then it doesn't show up in the model.summary()

    Args:
        input_dim (int): number of input features
        output_dim (int): number of output features
        units_per_layer (int, optional): number of units per layers. Defaults to 128.
        layers_per_block (int, optional): number of Dense layers before a BatchNormalisation Layer is added if batch_norm is True. Defaults to 3.
        n_blocks (int, optional): number of blocks. Defaults to 3.
        activation (str, optional): specify activation function. Only the following functions are implemented: ['relu', 'leaky_relu', 'prelu', 'elu', 'softplus', 'tanh', 'selu'] Defaults to 'relu'.
        leaky_alpha (float, optional): alpha parameter for leaky_relu activation function. Defaults to 0.3.
        batch_norm (bool, optional): If True then add a BatchNormalisation Layer at the end of each 'block'. Defaults to True.
        summary (bool, optional): If True then print model.summary(). Defaults to True.

    Raises:
        ValueError: Raised if activation function supplied is not in the 'allowed_activations'

    Returns:
        keras Sequential model: a keras Sequential model ready for compilation.
    """

    allowed_activations = ['relu', 'leaky_relu',
                           'prelu', 'elu', 'softplus', 'tanh', 'selu',
                           'srelu', 'srelu2', 'srelu3']

    if activation not in allowed_activations:
        raise ValueError(
            f"activation: ({activation}) not in allowed_activations: ({allowed_activations})")

    if batch_norm:
        use_bias = False
    else:
        use_bias = True

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Input(shape=(input_dim,)))
    for i in range(n_blocks):
        for j in range(layers_per_block):
            #   model.add(tf.keras.layers.Dense(units_per_layer, activation=activation, use_bias=use_bias))
            # separate out the activation function so that you can load a saved model with LeakyReLU
            # https://github.com/tensorflow/tfjs/issues/1093
            model.add(tf.keras.layers.Dense(
                units_per_layer, use_bias=use_bias))
            if activation == "relu":
                model.add(tf.keras.layers.ReLU())
            elif activation == "leaky_relu":
                model.add(tf.keras.layers.LeakyReLU(alpha=leaky_alpha))
            elif activation == "prelu":
                model.add(tf.keras.layers.PReLU())
            elif activation == "elu":
                model.add(tf.keras.layers.ELU())
            elif activation == "softplus":
                model.add(tf.keras.layers.Activation(
                    tf.keras.activations.softplus))
            elif activation == "tanh":
                model.add(tf.keras.layers.Activation(
                    tf.keras.activations.tanh))
            elif activation == "selu":
                model.add(tf.keras.layers.Activation(
                    tf.keras.activations.selu))
            elif activation == "srelu":
                model.add(pugna.activations.sReLU_Layer())
            elif activation == "srelu2":
                model.add(pugna.activations.sReLU_2_Layer())
            elif activation == "srelu3":
                model.add(pugna.activations.sReLU_3_Layer())
        if batch_norm:
            model.add(tf.keras.layers.BatchNormalization())
    model.add(tf.keras.layers.Dense(output_dim, activation='linear'))
    if summary:
        model.summary()
    return model


def compile_model(model, learning_rate=1e-3, optimizer=tf.keras.optimizers.Adam, loss='mse', metrics=['mse']):
    """compile a tf.keras model

    Args:
        model (tf.keras model): A tf.keras model
        learning_rate (float, optional): initial learning rate for optimiser. Defaults to 1e-3.
        optimizer (tf.keras.optimizer, optional): Specify optimizer. Defaults to tf.keras.optimizers.Adam.
        loss (str, optional): Specify loss function. Defaults to 'mse'.
        metrics (list, optional): specify list of metrics. Defaults to ['mse'].

    Returns:
        keras model: a compiled keras model
    """
    opt = optimizer(learning_rate=learning_rate)
    model.compile(loss=loss, optimizer=opt, metrics=metrics)

    return model
