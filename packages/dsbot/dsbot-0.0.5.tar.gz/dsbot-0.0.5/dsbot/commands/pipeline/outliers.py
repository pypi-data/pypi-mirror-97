import random
from sklearn import datasets

from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument
from ..base.predict import PredictCommand

from ..preprocess.extract_column import ColumnExtractCommand
from ..preprocess.remove_column import ColumnRemoveCommand

from ..metrics.accuracy import AccuracyCommand
from ..algoritms.pyod import *

from ..visualization.plot_scatter import ScatterPlotCommand


class OutliersPipeCommand(CommandWithArgs):

    tag = "outliers_pipe"
    patterns = [
        "analise de pontos extremos",
        "quais são os pontos extremos",
        "pontos extremos"
    ]

    def __init__(self, parent, task_manager):
        super(OutliersPipeCommand, self).__init__(parent, task_manager)
        self.responses = ["Fazendo uma analise de pontos extremos no dataset {0}."]
        self.user_config_tag = 'pipe'

        self.algorithms = {
            "abod": AbodAlgorithm,
            "pyod_autoencoder": AutoEncoderAlgorithm,
            "pyod_cblof": CblofAlgorithm,
            "pyod_hbos": HbosAlgorithm,
            "pyod_iforest": IForestAlgorithm,
            "pyod_knn": KnnAlgorithm,
            "pyod_lmdd": LmddAlgorithm,
            "pyod_loda": LodaAlgorithm,
        }

        self.complete = False

        self.dataset_name_arg = Argument({
            "parent": self,
            "name": 'dataset_name',
            "position": 1,
            "trigger": "dataset"
        })

        self.target_arg = Argument({
            "parent": self,
            "name": 'outline_clf',
            "position": 1,
            # Never extract from input text
            "trigger": "outlier classification column"
        })

        self.children = [
            self.dataset_name_arg,
            self.target_arg
        ]

    def run(self, context):
        dataset_name = self.dataset_name_arg.value
        dataframe = context[dataset_name]
        target = self.target_arg.value

        column_extraction = ColumnExtractCommand(parent=self, task_manager=self.task_manager)
        column_extraction.dataset_name = self.dataset_name_arg
        column_extraction.column_name = self.target_arg
        column_extraction.context_variable.value = "outliers_pipe_target"
        column_extraction.context_variable.complete = True
        column_extraction.complete = True

        column_extraction.run(context)
        # self.task_manager.add_task({
        #     'fn': column_extraction.run,
        #     'args': {
        #         'context': context,
        #     }
        # })

        self.children.append(column_extraction)

        column_deletion = ColumnRemoveCommand(parent=self, task_manager=self.task_manager)
        column_deletion.dataset_name = self.dataset_name_arg
        column_deletion.column_name = self.target_arg
        column_deletion.complete = True

        column_deletion.run(context)
        # self.task_manager.add_task({
        #     'fn': column_deletion.run,
        #     'args': {
        #         'context': context,
        #     }
        # })

        self.children.append(column_deletion)


        algorithms_accuracy = []
        best_acc = -1
        best_alg = ""
        for current_algorithm_name, current_algorithm in self.algorithms.items():
            algorithm = current_algorithm.algorithm
            algorithm = algorithm(current_algorithm.get_arg(dataframe=dataframe))
            algorithm.fit(dataframe)
            context["{0}_outliers_pipe_model".format(current_algorithm_name)] = algorithm

            predict = PredictCommand(parent=self, task_manager=self.task_manager)
            predict.dataset_name = self.dataset_name_arg
            predict.model_name.value = "{0}_outliers_pipe_model".format(current_algorithm_name)
            predict.model_name.complete = True
            predict.context_variable.value = "{0}_outliers_pipe_model_prediction".format(current_algorithm_name)
            predict.context_variable.complete = True
            predict.complete = True

            predict.run(context)
            # self.task_manager.add_task({
            #     'fn': predict.run,
            #     'args': {
            #         'context': context,
            #     }
            # })

            self.children.append(predict)

            accuracy = AccuracyCommand(parent=self, task_manager=self.task_manager)
            accuracy.y_true_arg.value = "outliers_pipe_target"
            accuracy.y_true_arg.complete = True
            accuracy.y_pred_arg.value = "{0}_outliers_pipe_model_prediction".format(current_algorithm_name)
            accuracy.y_pred_arg.complete = True
            accuracy.context_variable.value = "{0}_outliers_pipe_model_accuracy".format(current_algorithm_name)
            accuracy.context_variable.complete = True
            accuracy.complete = True

            accuracy.run(context)
            # self.task_manager.add_task({
            #     'fn': accuracy.run,
            #     'args': {
            #         'context': context,
            #     }
            # })

            self.children.append(accuracy)

            acc_value =context[accuracy.context_variable.value]
            algorithms_accuracy.append({
                "name":current_algorithm_name,
                "accuracy": acc_value
            })

            # update best result
            if(acc_value > best_acc):
                self.report("{0} obteve um resultado de {1} MELHOR do que o {2} do algoritmo {3}".format(current_algorithm_name,acc_value, best_acc, best_alg ))
                best_acc = acc_value
                best_alg = current_algorithm_name
            else:
                self.report("{0} deu {1} mais NAO melhorou o {2} do algoritmo {3}".format(current_algorithm_name,acc_value, best_acc, best_alg ))


            scatter_plot = ScatterPlotCommand(parent=self, task_manager=self.task_manager)
            scatter_plot.title = "{0} Algorithm".format(current_algorithm_name)
            scatter_plot.dataset_name = self.dataset_name_arg
            scatter_plot.colors.value = "{0}_outliers_pipe_model_prediction".format(current_algorithm_name)
            scatter_plot.colors.complete = True
            scatter_plot.x_axis.value = 'x1'
            scatter_plot.x_axis.complete = True
            scatter_plot.y_axis.value = 'x2'
            scatter_plot.y_axis.complete = True
            scatter_plot.complete = True

            scatter_plot.run(context)
            # self.task_manager.add_task({
            #     'fn': scatter_plot.run,
            #     'args': {
            #         'context': context,
            #     }
            # })

            self.children.append(scatter_plot)

        # Finally print the results
        # algorithms_accuracy = sorted(algorithms_accuracy, key=lambda k: k['accuracy'], reverse=True)
        # self.print_metrics(algorithms_accuracy)

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Begin: Outlines Analysis Pipeline")
        for child in self.children:
            child.generate_code(code_generator, context)
        code_generator.write("")
        code_generator.write("# End: Outlines Analysis Pipeline")

    def print_metrics(self, metrics):
        print("\tName\t|\tAccuracy")
        print("\t--------------------")
        for alg in metrics:
            print("\t{0}\t|\t{1}".format(alg['name'], alg['accuracy']))