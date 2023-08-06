from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class LowerUpperCommand(CommandWithArgs):

    tag = "lower_upper_case"
    patterns = [
        "Formate letras minusculas",
        "Transforme letras minusculas",
        "Formate letras maiusculas",
        "Transforme letras maiusculas",
    ]

    def __init__(self, parent, task_manager):
        super(LowerUpperCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso formatar os dados da coluna {x} para {y}."]
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

        self.word_case = Argument({
            "parent": self,
            "name": 'word_case',
            "required": True,
            "position": 1,
            "patterns": [
                'para (minuscula|maiuscula)',
                'letra (minuscula|maiuscula)'
            ]
        })

        self.children = [
            self.dataset_name,
            self.column_name,
            self.word_case
        ]

    def run(self, context):
        import numpy as np

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value
        word_case = self.word_case.value

        x = context[dataset_name][column_name]
        column_index=context[dataset_name].columns.get_loc(column_name)

        for index, value in x.items():
            try:
                current = context[dataset_name].iloc[index, column_index]
                if word_case == "minuscula":
                    current = current.lower()
                if word_case == "maiuscula":
                    current = current.upper()
                context[dataset_name].iloc[index, column_index] = current
            except:
                pass


    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Select column from dataset")

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        # code_generator.write("{0} = {1}['{2}']".format(context_variable, dataset_name, column_name))

