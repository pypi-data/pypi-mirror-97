import tensorflow as tf
import pugna.activations
import pugna.layers


def build_model(input_dim, output_dim, nlayers, units, nscales, activations, dropouts, batch_norms, scale_names):
    """
    Args:
        input_dim: int, number of input features
        output_dim: int, number of output features
        nlayers: ints, number of hidden layers
        units: list of ints, number of units in each layer, len = nlayers
        nscales: list of int, number of scales in each layer in an MscaleDNN, len = nlayers
            if nscales = 1 then this should be the same as a standard Dense layer.
        activations: list of str, what activation to use in each hidden layer
        dropouts: list of floats, dropout fraction in each layer. use 0. for no dropout
            dropout is applied AFTER activations
        batch_norms: list of bools, add batch normalisation to a particular hidden layer.
            batch norm is applied BEFORE activations
        scale_names: list of strings. Mscale layer option, choices: ['linear', 'base2']

    Raises:
        ValueError: Raised if activation function supplied is not in the 'allowed_activations'

    Returns:
        a tf.keras.model

    example

    model = build_model(
        1,
        1,
        3,
        [128, 128, 128],
        [10, 10, 10],
        ['s2relu', 's2relu', 's2relu'],
        [0, 0, 0.2],
        [False, True, True],
        ['linear','linear','linear']
    )

    # you don't have to specify each list fully.
    # if there is only a single value then it will get
    # broadcasted to the size of nlayers
    model = build_model(
        1,
        1,
        4,
        [128, 128, 64, 32],
        [10],
        ['s2relu'],
        [0],
        [False],
        ['base2']
    )
    """

    allowed_activations = ['s2relu', 'relu', 'tanh']

    for activation in activations:
        if activation not in allowed_activations:
            raise ValueError(
                f"activation: ({activation}) not in allowed_activations: ({allowed_activations})")

    model = tf.keras.models.Sequential()

    model.add(tf.keras.layers.InputLayer(input_shape=(input_dim,)))

    for n in range(nlayers):
        model.add(pugna.layers.Mscale(units[n], nscales[n], scale_names[n]))
        if batch_norms[n]:
            model.add(tf.keras.layers.BatchNormalization())
        if activations[n] == 's2relu':
            model.add(tf.keras.layers.Activation(pugna.activations.s2relu))
        elif activations[n] == 'relu':
            model.add(tf.keras.layers.ReLU())
        elif activations[n] == 'tanh':
            model.add(tf.keras.layers.Activation(tf.keras.activations.tanh))
        if dropouts[n]:
            model.add(tf.keras.layers.Dropout(dropouts[n]))

    model.add(tf.keras.layers.Dense(output_dim, activation="linear"))

    return model
