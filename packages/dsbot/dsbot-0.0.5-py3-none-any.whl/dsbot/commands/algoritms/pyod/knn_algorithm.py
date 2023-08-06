from pyod.models.knn import KNN


class KnnAlgorithm:
    algorithm = KNN
    name = "KNN"
    import_code = "from pyod.models.knn import KNN"

    def __init__(self):
        pass

    @classmethod
    def get_arg(cls, **args):
        return {}

    @classmethod
    def get_args_code(cls, **args):
        return ''
