from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument

class ColumnExtractCommand(CommandWithArgs):

    tag = "column_extract"
    patterns = [
        "Guarda a coluna",
        "Seleciona uma coluna",
        "Sava a columna",
    ]

    def __init__(self, parent, task_manager):
        super(ColumnExtractCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso extrair a coluna {x} e guardar em {y}."]
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

        self.context_variable = Argument({
            'parent': self,
            'name': 'variable_name',
            'trigger': 'guarda em',
            'position': 1
        })

        self.children = [
            self.dataset_name,
            self.column_name,
            self.context_variable
        ]

    def run(self, context):

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value
        context_variable = self.context_variable.value

        x = context[dataset_name][column_name]
        context[context_variable] = x

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Select column from dataset")

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value
        context_variable = self.context_variable.value

        code_generator.write("{0} = {1}['{2}']".format(context_variable, dataset_name, column_name))

