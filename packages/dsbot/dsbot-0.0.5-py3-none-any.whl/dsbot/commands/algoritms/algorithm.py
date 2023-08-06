from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument

from pyod.models.abod import ABOD
from pyod.models.cblof import CBLOF
from pyod.models.auto_encoder import AutoEncoder

from .pyod import *

class AlgorithmCommand(CommandWithArgs):

    tag = "algorithm"
    patterns = [
        "Queria rodar o algoritmo",
        "vamos a aplicar o algoritmo",
        "Queria rodar o algoritmo",
        "Treina o algoritmo",
        "Vamos dar fit do algoritmo",
        "Executa o algoritmo"
    ]

    def __init__(self, parent, task_manager):
        super(AlgorithmCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso rodar o algortimo {0} no dataset {1} e guardar o resultao em {2}."]
        self.user_config_tag = 'algorithm'
        self.algorithms = {
            'abod': AbodAlgorithm,
            'cblof': CblofAlgorithm,
            'autoencoder': AutoEncoderAlgorithm,
            'hhos': HbosAlgorithm,
            'iforest': IForestAlgorithm,
            'knn': KnnAlgorithm,
            'lmdd': LmddAlgorithm,
            'loda': LodaAlgorithm
        }

        self.complete = False

        self.algorithm_name = Argument({
            'parent': self,
            'name': 'algorithm_name',
            'trigger': 'algoritmo',
            'position': 1
        })

        self.dataset_name = Argument({
            'parent': self,
            'name': 'dataset_name',
            'trigger': 'dataset',
            'position': 1
        })

        self.context_variable = Argument({
            'parent': self,
            'name': 'variable_name',
            'trigger': 'guarda em',
            'position': 1
        })

        self.children = [
            self.algorithm_name,
            self.dataset_name,
            self.context_variable
        ]

    def run(self, context):

        algorithm_name = self.algorithm_name.value
        dataset_name = self.dataset_name.value
        context_variable = self.context_variable.value

        algorithm = self.algorithms[algorithm_name].algorithm
        dataframe = context[dataset_name]

        algorithm_agrs = self.algorithms[algorithm_name].get_arg(dataframe=dataframe)
        clf = algorithm(**algorithm_agrs)
        clf.fit(dataframe)
        context[context_variable] = clf

    def generate_code(self, code_generator, context):

        algorithm_name = self.algorithm_name.value
        algorithm = self.algorithms[algorithm_name]
        dataset_name = self.dataset_name.value
        dataframe = context[dataset_name]

        code_generator.write("")
        code_generator.write("# Fit the {0} algorithm".format(algorithm.name))
        code_generator.write(algorithm.import_code)

        dataset_name = self.dataset_name.value
        context_variable = self.context_variable.value

        algorithm_args = algorithm.get_args_code(dataframe=dataframe)
        code_generator.write("{0} = {1}({2})".format(context_variable, algorithm.name, algorithm_args))
        code_generator.write("{0}.fit({1})".format(context_variable,dataset_name))

