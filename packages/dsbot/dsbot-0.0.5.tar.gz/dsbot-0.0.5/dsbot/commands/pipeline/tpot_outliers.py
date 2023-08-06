import random
import os
from tpot import TPOTClassifier

from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument
from ..base.predict import PredictCommand

from ..preprocess.extract_column import ColumnExtractCommand
from ..preprocess.remove_column import ColumnRemoveCommand

from ..metrics.accuracy import AccuracyCommand

from ..visualization.plot_scatter import ScatterPlotCommand

class TPOTOutliersPipeCommand(CommandWithArgs):

    tag = "outliers_pipe"
    patterns = [
        "analise de pontos extremos",
        "quais são os pontos extremos",
        "pontos extremos"
    ]

    def __init__(self, parent, task_manager):
        super(TPOTOutliersPipeCommand, self).__init__(parent, task_manager)
        self.responses = ["Fazendo uma analise de pontos extremos no dataset {0}."]
        self.user_config_tag = 'pipe'

        from sklearn.naive_bayes import BernoulliNB
        from pyod.models.abod import ABOD
        self.tpot_config = {
            'pyod.models.abod.ABOD': {
                'contamination': [0.1, 0.2, 0.3, 0.4],
                'n_neighbors': [8, 9, 10, 11, 12]
            }
            ,
            'pyod.models.cblof.CBLOF': {
                'contamination': [0.1, 0.2, 0.3, 0.4],
                'n_clusters': [8, 9, 10, 11, 12]
            }
        }
        self.tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2, config_dict=self.tpot_config)

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

        self.column_extraction = ColumnExtractCommand(parent=self, task_manager=self.task_manager)
        self.column_deletion = ColumnRemoveCommand(parent=self, task_manager=self.task_manager)


        self.children = [
            self.dataset_name_arg,
            self.target_arg
        ]

    def run(self, context):
        dataset_name = self.dataset_name_arg.value
        target = self.target_arg.value

        self.column_extraction.dataset_name = self.dataset_name_arg
        self.column_extraction.column_name = self.target_arg
        self.column_extraction.context_variable.value = "outliers_pipe_target"
        self.column_extraction.context_variable.complete = True
        self.column_extraction.complete = True
        self.column_extraction.run(context)
        self.children.append(self.column_extraction)

        self.column_deletion.dataset_name = self.dataset_name_arg
        self.column_deletion.column_name = self.target_arg
        self.column_deletion.complete = True
        self.column_deletion.run(context)
        self.children.append(self.column_deletion)

        # tpot = TPOTClassifier(generations=5, population_size=20, verbosity=2)

        self.tpot.fit(context[dataset_name], context['outliers_pipe_target'])
        print(self.tpot.score(context[dataset_name], context['outliers_pipe_target']))


    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Begin: Outlines Analysis Pipeline")

        self.column_extraction.generate_code(code_generator, context)
        self.column_deletion.generate_code(code_generator, context)

        self.tpot.export('data/tpot_digits_pipeline.py')

        tpot_code_file = open('data/tpot_digits_pipeline.py', 'r')
        Lines = tpot_code_file.readlines()
        for line in Lines:
            line.replace(r'\n', "")
            code_generator.write(line)
        tpot_code_file.close()
        # os.remove('data/tpot_digits_pipeline.py')

        code_generator.write("")
        code_generator.write("# End: Outlines Analysis Pipeline")
