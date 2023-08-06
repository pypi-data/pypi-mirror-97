import tensorflow as tf


class PrintDot(tf.keras.callbacks.Callback):
    """
    Display training progress by printing a single dot for
    each completed epoch.
    """

    def on_epoch_end(self, epoch, logs) -> None:
        """
        `on_epoc_end` hook to take the epoch number and logs.
        This will run whenever the training loop finishes an epoch.
        """
        if epoch % 100 == 0:
            print("", flush=True)
        print(".", end="", flush=True)
