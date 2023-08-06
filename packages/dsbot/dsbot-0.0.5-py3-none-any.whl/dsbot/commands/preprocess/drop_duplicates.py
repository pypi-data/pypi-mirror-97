from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class DropDuplicateCommand(CommandWithArgs):

    tag = "drop_duplicate"
    patterns = [
        "Elimine as linhas duplicadas",
        "Elimine as linhas con valores duplicados ",
        "Remova as linhas repetidas",
    ]

    def __init__(self, parent, task_manager):
        super(DropDuplicateCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso eliminar as linhas duplicadas com base na coluna {x}"]
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

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        df = context[dataset_name]

        try:
            df.drop_duplicates(subset=[column_name], inplace=True)
        except Exception as e:
            print(e)

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Select column from dataset")

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        # code_generator.write("{0} = {1}['{2}']".format(context_variable, dataset_name, column_name))

