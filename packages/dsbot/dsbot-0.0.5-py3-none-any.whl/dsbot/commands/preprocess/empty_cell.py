from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class CellEmptyCommand(CommandWithArgs):

    tag = "empty_cell"
    patterns = [
        "substitua os espaços brancos",
        "troque os espaços vazios",
        "troque os espaços em branco",
        "troque os valores null",
        "substitua os valores nan",
    ]

    def __init__(self, parent, task_manager):
        super(CellEmptyCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso substitua os espaços vazios da coluna {x} pela {y}."]
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

        self.cell_value = Argument({
            "parent": self,
            "name": 'cell_value',
            "required": True,
            "position": 1,
            "patterns": [
                'pela (mediana|media)',
                'por a (mediana|media)'
            ]
        })

        self.children = [
            self.dataset_name,
            self.column_name,
            self.cell_value
        ]

    def run(self, context):
        import numpy as np

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value
        cell_value = self.cell_value.value

        x = context[dataset_name][column_name]
        column_index=context[dataset_name].columns.get_loc(column_name)

        sum = 0
        total = len(x)
        wrong_lines = []
        for index, value in x.items():
            try:
                current= float(value)
                if not np.isnan(current):
                    # print("{0}: {1}".format(index,current))
                    sum = sum + current
                else:
                    wrong_lines.append(index)
            except:
                wrong_lines.append(index)

        replace = 0
        if cell_value == "media":
            replace = sum/total

        # replace wrong values.
        context[dataset_name].iloc[wrong_lines, column_index] = replace


    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Select column from dataset")

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value
        cell_value = self.cell_value.value

        # code_generator.write("{0} = {1}['{2}']".format(context_variable, dataset_name, column_name))

