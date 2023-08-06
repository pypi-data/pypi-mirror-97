from pyod.models.abod import ABOD


class AbodAlgorithm:
    algorithm = ABOD
    name = "ABOD"
    import_code = "from pyod.models.abod import ABOD"

    def __init__(self):
        pass

    @classmethod
    def get_arg(cls, **args):
        return {
            'method': "fast"
        }

    @classmethod
    def get_args_code(cls, **args):
        return 'method=fast'
