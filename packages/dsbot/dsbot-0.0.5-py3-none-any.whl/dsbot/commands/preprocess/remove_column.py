from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class ColumnRemoveCommand(CommandWithArgs):

    tag = "column_deletion"
    patterns = [
        "Apaga a coluna",
        "Elimina a coluna",
        "Remove uma coluna",
        "Deleta a columna",
    ]

    def __init__(self, parent, task_manager):
        super(ColumnRemoveCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso apagar a coluna {0} do dataset {1}."]
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
            self.column_name,
        ]

    def run(self, context):

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        # replace the context variable
        dataframe = context[dataset_name]
        context[dataset_name] = dataframe.loc[:, dataframe.columns != column_name]

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Remove column from dataset")

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        code_generator.write("{0} = {0}.loc[:, {0}.columns != '{1}']".format(dataset_name, column_name))


