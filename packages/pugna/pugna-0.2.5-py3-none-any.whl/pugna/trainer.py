import tensorflow as tf
import numpy as np
from pugna import training_utils


class IterativeTraining(object):

    def __init__(self):
        """
        initialises callbacks, stategy to None
        init_counter to zero
        and applies `apply_default_settings()`
        """
        self.callbacks = None
        self.strategy = None
        self.init_counter = 0  # counts number of times self.initialise is called

        self.apply_default_settings()

    def apply_default_settings(self):
        self.set_loss('mse')
        self.set_metrics(['mse'])

    def initialise(self, n_iter, epochs=None, learning_rates=None, batch_sizes=None, ts_sizes=None):
        """
        params
        n_iter {int}: number of times to iterate.
            Used to check length of other lists
        use this to change n_iter between training sessions
        """
        self.set_n_iter(n_iter)

        self.set_epochs(epochs)
        self.set_learning_rates(learning_rates)
        self.set_batch_sizes(batch_sizes)
        self.set_ts_sizes(ts_sizes)

        self.init_counter += 1

        if self.init_counter == 1:
            # if counter is 1 then setup lists
            # attributes with "all_" prefix
            # persist through training loops
            self.all_history = []
            self.all_epochs_ranges = []
            self.all_epochs = []
            self.epoch_counter = 0

            self.all_learning_rates = []
            self.all_batch_sizes = []
            self.all_ts_sizes = []

    @property
    def info(self):
        return f"""
init_counter: {self.init_counter}
n_iter: {self.n_iter}
epochs: {self.epochs}
learning_rates: {self.learning_rates}
batch_sizes: {self.batch_sizes}
ts_sizes: {self.ts_sizes}
        """

    def set_epochs(self, epochs):
        self.epochs = self._set_input_args(epochs, 100)
        self._check_intput_args(self.epochs)

    def set_learning_rates(self, learning_rates):
        self.learning_rates = self._set_input_args(learning_rates, 1e-3)
        self._check_intput_args(self.learning_rates)

    def set_batch_sizes(self, batch_sizes):
        self.batch_sizes = self._set_input_args(batch_sizes, None)
        self._check_intput_args(self.batch_sizes)

    def set_ts_sizes(self, ts_sizes):
        self.ts_sizes = self._set_input_args(ts_sizes, None)
        self._check_intput_args(self.ts_sizes)

    def set_n_iter(self, n_iter):
        self.n_iter = n_iter

    def _reset_init_counter(self):
        self.init_counter = 0

    def _set_input_args(self, value, default_value):
        """
        if value is a list then return the list
        elif value is not a list, assume it's a single number
        and we convert it to a list of length self.n_iter
        If value is None then we use default_value
        """
        if type(value) == list:
            return value
        elif value is None:
            value = default_value
        return [value] * self.n_iter

    def _check_intput_args(self, value):
        assert len(value) == self.n_iter

    # def set_model(self, model):
    #     self.model = model

    def set_loss(self, loss_func):
        self.loss = loss_func

    def set_optimiser(self, optimiser):
        self.optimiser = optimiser

    def set_callbacks(self, callbacks):
        if self.callbacks:
            self.callbacks.append(callbacks)
        else:
            self.callbacks = callbacks

    def set_metrics(self, metrics):
        self.metrics = metrics

    def set_strategy(self, strategy):
        """
        used for TPU / multi-GPU
        https://www.tensorflow.org/guide/tpu
        https://keras.io/getting_started/faq/#how-can-i-train-a-keras-model-on-multiple-gpus-on-a-single-machine
        """
        self.strategy = strategy

    def set_build_model_func(self, build_model_func):
        """
        build_model_func is any function that returns a tf.keras.Model
        """
        self.build_model_func = build_model_func

    def build_model(self):
        try:
            return self.build_model_func()
        except AttributeError as error:
            print(error)
            print("please supply a 'build_model_func' using 'set_build_model_func'")
            raise

    def compile(self):
        self.model.compile(
            loss=self.loss, optimizer=self.current_opt, metrics=self.metrics)

    def build_compile(self):
        """
        sets the model attribute
        """
        self.model = self.build_model()
        self.model.compile(
            loss=self.loss, optimizer=self.current_opt, metrics=self.metrics)

    def _make_full_history(self):
        """
        concatenates epochs and histories
        from each iteration into continuous arrays
        """
        self.full_epochs = np.concatenate(
            [list(ep) for ep in self.all_epochs_ranges])

        keys = self.all_history[0].history.keys()
        self.full_history = {}
        for key in keys:
            value = np.concatenate(
                [list(hh.history[key]) for hh in self.all_history]
            )
            self.full_history.update({key: value})

    def _training_step(self, X, y, epochs, learning_rate, batch_size, fit_verbose, validation_data):
        """
        one iteration
        calls:
            model.compile
            model.fit
        """

        self.current_opt = self.optimiser.from_config(
            {'learning_rate': learning_rate})

        if self.strategy is not None:
            with self.strategy.scope():
                # self.build_compile()
                self.compile()
        else:
            # self.build_compile()
            self.compile()

        self.current_history = self.model.fit(
            X,
            y,
            epochs=epochs,
            batch_size=batch_size,
            callbacks=self.callbacks,
            verbose=fit_verbose,
            validation_data=validation_data
        )

        self.all_history.append(self.current_history)
        self.all_epochs_ranges.append(
            range(self.epoch_counter, self.epoch_counter + epochs))

        self.epoch_counter += epochs

    def train(self, X, y, verbose, fit_verbose=0, validation_data=None):

        if self.strategy is not None:
            with self.strategy.scope():
                self.model = self.build_model()
                # self.build_compile()
        else:
            self.model = self.build_model()
            # self.build_compile()

        for n in range(self.n_iter):
            if verbose:
                print(f"\nworking: {n} / {self.n_iter - 1}")

            if self.ts_sizes[n] is not None:
                Xfit, yfit = training_utils.shuffle_data(
                    X, y, size=self.ts_sizes[n], seed=None)
            else:
                Xfit = X.copy()
                yfit = y.copy()

            self._training_step(
                Xfit,
                yfit,
                epochs=self.epochs[n],
                learning_rate=self.learning_rates[n],
                batch_size=self.batch_sizes[n],
                fit_verbose=fit_verbose,
                validation_data=validation_data
            )
            self.all_epochs.append(self.epochs[n])
            self.all_learning_rates.append(self.learning_rates[n])
            self.all_batch_sizes.append(self.batch_sizes[n])
            self.all_ts_sizes.append(self.ts_sizes[n])

            if verbose:
                self.current_error = self.current_history.history['loss'][-1]
                print(f"\ncurrent error: {self.current_error}")

        if verbose:
            print("\nrunning: self._make_full_history()")
        self._make_full_history()

        print("\ndone!")

    def plot_loss(self, figsize=(10, 8)):
        import matplotlib
        import matplotlib.pyplot as plt
        matplotlib.rcParams.update({"font.size": 16})

        fig = plt.figure(figsize=figsize)
        for i in range(len(self.all_epochs_ranges)):
            plt.scatter(
                self.all_epochs_ranges[i], self.all_history[i].history['loss'], label=self.all_learning_rates[i])
        plt.plot(self.full_epochs,
                 self.full_history['loss'], c='k', label='loss')

        if 'val_loss' in self.full_history:
            plt.plot(
                self.full_epochs, self.full_history['val_loss'], c='k', ls='--', label='val loss')

        plt.yscale('log')
        plt.xlabel("epochs")
        plt.ylabel("Loss")
        plt.axhline(self.current_error, ls='--', c='k')

        plt.legend(loc='center left', fancybox=True,
                   framealpha=0.9, bbox_to_anchor=(1.05, 0.5))
        return fig
