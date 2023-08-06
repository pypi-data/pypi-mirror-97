from pyod.models.iforest import IForest


class IForestAlgorithm:
    algorithm = IForest
    name = "IForest"
    import_code = "from pyod.models.iforest import IForest"

    def __init__(self):
        pass

    @classmethod
    def get_arg(cls, **args):
        return {}

    @classmethod
    def get_args_code(cls, **args):
        return ''
