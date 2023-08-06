from pyod.models.cblof import CBLOF


class CblofAlgorithm:
    algorithm = CBLOF
    name = "CBLOF"
    import_code = "from pyod.models.cblof import CBLOF"

    def __init__(self):
        pass

    @classmethod
    def get_arg(cls, **args):
        return {}

    @classmethod
    def get_args_code(cls, **args):
        return ''