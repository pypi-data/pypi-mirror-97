from pyod.models.hbos import HBOS


class HbosAlgorithm:
    algorithm = HBOS
    name = "HBOS"
    import_code = "from pyod.models.hbos import HBOS"

    def __init__(self):
        pass

    @classmethod
    def get_arg(cls, **args):
        return {}

    @classmethod
    def get_args_code(cls, **args):
        return ''
