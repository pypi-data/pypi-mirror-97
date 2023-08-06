from pyod.models.lmdd import LMDD


class LmddAlgorithm:
    algorithm = LMDD
    name = "LMDD"
    import_code = "from pyod.models.lmdd import LMDD"

    def __init__(self):
        pass

    @classmethod
    def get_arg(cls, **args):
        return {}

    @classmethod
    def get_args_code(cls, **args):
        return ''
