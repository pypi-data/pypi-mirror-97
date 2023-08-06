from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class NormalizeColumnCommand(CommandWithArgs):

    tag = "normalize_column"
    patterns = [
        "vamos normalizar",
        "aplique uma normalizaçao",
    ]

    def __init__(self, parent, task_manager):
        super(NormalizeColumnCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso normalizar os dados da coluna {x} entre 0 e 1."]
        self.user_config_tag = 'preprocessing'

        self.complete = False

        self.dataset_name = Argument({
            'parent': self,
            'name': 'dataset_name',
            'trigger': 'dataset',
            'position': 1
        })

        self.column_name = Argument({
            'parent': self,
            'name': 'column_name',
            'trigger': 'coluna',
            'position': 1
        })

        self.children = [
            self.dataset_name,
            self.column_name
        ]

    def run(self, context):
        import numpy as np

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        x = context[dataset_name][column_name]
        column_index=context[dataset_name].columns.get_loc(column_name)


        try:
            x = np.array(x, dtype=float)
            min_value = np.min(x)
            max_value = np.max(x)
            new_column = (x-min_value)/(max_value-min_value)
            # replace the column
            context[dataset_name].iloc[:, column_index] = new_column
        except Exception as e:
            print(e)

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Select column from dataset")

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        # code_generator.write("{0} = {1}['{2}']".format(context_variable, dataset_name, column_name))

