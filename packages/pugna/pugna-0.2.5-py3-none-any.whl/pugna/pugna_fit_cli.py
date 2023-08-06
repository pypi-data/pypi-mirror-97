def insert_pugna_fit_option_group(parser):
    """command line interface tool for pugna_fit exe.
    Use this to add command line options for the pugna_fit exe.

    Args:
        parser (object): argparse instance

    Returns:
        pugna_fit_group (object): argparse instance containing pugna_fit options
    """

    pugna_fit_group = parser.add_argument_group("pugna_fit ANN arguments")

    pugna_fit_group.add_argument("--epochs", type=int, default=100,
                                 help="number of epochs to run for")

    pugna_fit_group.add_argument("--n-blocks", type=int, default=3,
                                 help="number of blocks")
    pugna_fit_group.add_argument("--units-per-layer", type=int, default=256,
                                 help="number of units per layers")
    pugna_fit_group.add_argument("--layers-per-block", type=int, default=3,
                                 help="number of Dense layers before a BatchNormalisation Layer is added if batch_norm is True")
    pugna_fit_group.add_argument("--activation", type=str, default='leaky_relu',
                                 help="name of activation function for each layer",
                                 choices=['relu', 'leaky_relu', 'prelu',
                                          'elu', 'softplus', 'tanh', 'selu',
                                          'srelu', 'srelu2', 'srelu3']
                                 )
    pugna_fit_group.add_argument("--leaky-relu-alpha", type=float, default=0.3,
                                 help="leaky-relu alpha parameter")

    pugna_fit_group.add_argument("--learning-rate", type=float, default=0.001,
                                 help="learning rate. If using lrs then this is the initial learning rate.")

    pugna_fit_group.add_argument("--use-lrs", help="use learning rate schedular. By default this is false.",
                                 action="store_true")
    pugna_fit_group.add_argument("--lrs-final-learning-rate", type=float, default=1e-5,
                                 help="final learning rate.")
    pugna_fit_group.add_argument("--lrs-decay-rate", type=int, default=10,
                                 help="""learning rate schedular (lrs) option.
                        factor by which learning rate decays
                        """)
    pugna_fit_group.add_argument("--lrs-decay-steps", type=int, default=1000,
                                 help="""learning rate schedular (lrs) option.
                        number of epochs before decaying.
                        """)

    pugna_fit_group.add_argument("--batch-norm",
                                 help="""add BatchNormalization layers in each hidden
                        layer before activation function. Default is false.""",
                                 action="store_true")

    pugna_fit_group.add_argument("--optimizer", type=str, default='Adam',
                                 help="name of optimizer to use",
                                 choices=['Adam', 'Nadam', 'Adadelta', 'Adagrad', 'Adamax', 'RMSprop', 'SGD'])

    pugna_fit_group.add_argument("--loss", type=str, default='mse',
                                 help="name of loss function to use",
                                 choices=['mse', 'mape'])

    pugna_fit_group.add_argument("--batch-size-factor", type=float, default=1,
                                 help="""mini-batch size specified by positive factor.
                        batch size is calculated as X.shape[0] / batch_size_factor
                        If 1 then mini-batch is the entire data set.""")

    return pugna_fit_group
