import numpy as np
import tensorflow as tf


def shuffle_data(X, y, size=None, seed=None):
    """
    X has a shape (N, M)
    y has a shape (N, 1)
    returns arrays of shape (size, M), (size, 1)
    which has been shuffled
    """
    ndim = X.shape[1]
    stacked_and_shuffled = tf.random.shuffle(
        np.column_stack([X, y]), seed=seed).numpy()
    Xnew = stacked_and_shuffled[:, :ndim]
    ynew = stacked_and_shuffled[:, -1]
    if size is None:
        return Xnew, ynew[..., np.newaxis]
    else:
        return Xnew[:size], ynew[:size][..., np.newaxis]
