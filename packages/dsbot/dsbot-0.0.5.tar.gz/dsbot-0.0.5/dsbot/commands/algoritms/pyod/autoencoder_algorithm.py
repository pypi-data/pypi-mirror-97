from pyod.models.auto_encoder import AutoEncoder


class AutoEncoderAlgorithm:
    algorithm = AutoEncoder
    name = "AutoEncoder"
    import_code = "from pyod.models.auto_encoder import AutoEncoder"

    def __init__(self):
        pass

    @classmethod
    def get_arg(cls, **args):
        dataframe = args['dataframe']
        return {
            'hidden_neurons': [len(dataframe.columns), 32, 32, len(dataframe.columns)]
        }

    @classmethod
    def get_args_code(cls, **args):
        dataframe = args['dataframe']
        return 'hidden_neurons = [{0}, 32, 32, {0}]'.format(len(dataframe.columns)),
