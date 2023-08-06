import tensorflow as tf
import pickle


def save_model_json(model, model_name):
    # serialize model to json
    json_model = model.to_json()
    # save the model architecture to JSON file
    with open(f'{model_name}.json', 'w') as json_file:
        json_file.write(json_model)
    # saving the weights of the model
    model.save_weights(f'{model_name}_weights.h5')


def load_model_json(model_name, custom_objects=None):
    """[summary]


    Args:
        model_name ([type]): [description]
        custom_objects ([dict], optional): Dictionary to pass to tf.keras.models.model_from_json.
        Use it to specify things like LeakyReLU.
        See: https://stackoverflow.com/questions/55364954/keras-load-model-cant-recognize-tensorflows-activation-functions
        See: https://github.com/tensorflow/tfjs/issues/1093
        Defaults to None.

    Returns:
        [type]: [description]
    """
    # Reading the model from JSON file
    with open(f'{model_name}.json', 'r') as json_file:
        json_savedModel = json_file.read()
    # load the model architecture
    model = tf.keras.models.model_from_json(
        json_savedModel, custom_objects=custom_objects)
    # model.summary()
    model.load_weights(f'{model_name}_weights.h5')
    return model


def save_model_h5(model, model_name):
    """save keras model as h5 file

    Args:
        model (keras model): [description]
        model_name (str): output file name will be f"{model_name}.h5"
    """
    model.save(f'{model_name}.h5')


def load_model_h5(filename, custom_objects=None):
    """load h5 model

    Args:
        filename (str): h5 file containing saved keras model
        custom_objects ([dict], optional): Dictionary to pass to tf.keras.models.load_model.
    """
    return tf.keras.models.load_model(filename, custom_objects=custom_objects)


def save_model_checkpoint(model, model_name, num, zpad='04'):
    """
    name format: '{model_name}+checkpoint_0001.h5'
    """
    # saving the smodel's architecture, weights, and training configuration in a single file/folder.
    model.save(f'{model_name}_checkpoint_' + format(num, zpad) + '.h5')


def load_model_checkpoint(model_name, num, zpad='04', custom_objects=None):
    """
    name format: '{model_name}+checkpoint_0001.h5'
    custom_objects ([dict], optional): Dictionary to pass to tf.keras.models.load_model.
    """
    # loading the model from the HDF5 file
    model = tf.keras.models.load_model(
        f'{model_name}_checkpoint_' + format(num, zpad) + '.h5', custom_objects=custom_objects)
    return model


def save_history(history, filename):
    """saves the History.history dictionary of a model.fit() to a pickle file

    Args:
        history (dict): History.history dictionary, output from model.fit().
        filename (str): full path and name output pickle file
    """

    with open(filename, 'wb') as pfile:
        pickle.dump(history, pfile)


def load_history(filename):
    """load the history.history dictionary of a model.fit() from a pickle file

    Args:
        filename (str): full path and name output pickle file

    Returns:
        history (dict): training history
    """

    with open(filename, 'rb') as pfile:
        history = pickle.load(pfile)

    return history

def save_datetime(value, filename):
    """saves the datetime to a pickle file

    Args:
        value (datetime):
        filename (str): full path and name output pickle file
    """
    with open(filename, 'wb') as f:
        pickle.dump(value, f)

def load_datetime(filename):
    """load the datetime from a pickle file

    Args:
        filename (str): full path and name output pickle file

    Returns:
        value (datetime): datetime
    """
    with open(filename, 'rb') as f:
        value = pickle.load(f)
    return value
