from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument

class WhiteSpacesCommand(CommandWithArgs):

    tag = "white_spaces"
    patterns = [
        "remova espaços branco adicionais",
        "elimine espaços em branco do começo e fim",
    ]

    def __init__(self, parent, task_manager):
        super(WhiteSpacesCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso substituir os espaços em branco adicionais da coluna {x}."]
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

        for index, value in x.items():
            try:
                current = context[dataset_name].iloc[index, column_index]
                context[dataset_name].iloc[index, column_index] = current.strip()
            except:
                pass


    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Select column from dataset")

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        # code_generator.write("{0} = {1}['{2}']".format(context_variable, dataset_name, column_name))

