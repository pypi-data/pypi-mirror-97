from pyod.models.loda import LODA


class LodaAlgorithm:
    algorithm = LODA
    name = "LODA"
    import_code = "from pyod.models.loda import LODA"

    def __init__(self):
        pass

    @classmethod
    def get_arg(cls, **args):
        return {}

    @classmethod
    def get_args_code(cls, **args):
        return ''
