import sklearn.preprocessing
import numpy as np


def make_scalers(X, method="MinMaxScaler", feature_range=(0, 1)):
    """This function takes an input array, X, and returns
    a list of sklearn scalers for each input feature/dimension.

    Arguments:
        X {np.ndarray} -- data to make scalers for.
        The shape should be (N,M) where
        N is the number of entries or samples.
        M is the number of features/dimensionality

    Keyword Arguments:
        method {str} -- method to use to scale data.
        common choices are "MinMaxScaler" or "StandardScaler".
        But in theory any `sklearn.preprocessing` scaler method should work
         (default: {"MinMaxScaler"})
        feature_range {tuple} -- (min, max), default=(0, 1)
            Only applicable for method='MinMaxScaler'

    Returns:
        list -- a least of length M of sklearn.preprocessing.[METHOD].
        The preprocessing scaler for each feature.
    """

    N, M = X.shape
    scalers = []


    # make a scaler for each feature/dimension
    for i in range(M):
        if method == "MinMaxScaler":
            scaler_func = sklearn.preprocessing.MinMaxScaler(feature_range=feature_range)
        else:
            scaler_func = getattr(sklearn.preprocessing, method)()
        scalers.append(scaler_func)
        scalers[i].fit(X[:, i].reshape(-1, 1))

    return scalers


def apply_scaler(X, scalers):
    """
    applies the scalers to X
    N, M = X.shape
    N = number of entries
    M = dimensionality
    """
    N, M = X.shape

    X_scaled = np.zeros(shape=(N, M))

    for i in range(M):
        X_scaled[:, i] = scalers[i].transform(
            X[:, i].reshape(-1, 1)).reshape(1, -1)

    return X_scaled


def apply_inverse_scaler(X_scaled, scalers):
    """
    applies the inverse scalers to X_scaled
    N, M = X.shape
    N = number of entries
    M = dimensionality
    """
    N, M = X_scaled.shape

    X = np.zeros(shape=(N, M))

    for i in range(M):
        X[:, i] = scalers[i].inverse_transform(
            X_scaled[:, i].reshape(-1, 1)).reshape(1, -1)

    return X


def save_scalers(Scalers, filename):
    """save sklearn.preprocessing scalers to a .npy file

    Arguments:
        Scalers {list} -- list of sklearn.preprocessing scalers
        filename {str} -- output filename
    """

    np.save(filename, Scalers)


def load_scalers(filename, allow_pickle=True):
    """load sklearn.preprocessing scalers from a .npy file

    Arguments:
        filename {str} -- .npy file to load

    Keyword Arguments:
        allow_pickle {bool} -- allow_pickle when loading (default: {True})

    Returns:
        list -- a list of sklearn.preprocessing scalers
    """
    return np.load(filename, allow_pickle=allow_pickle)
