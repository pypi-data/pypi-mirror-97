from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class SortColumnCommand(CommandWithArgs):

    tag = "sort_column"
    patterns = [
        "Ordene os valores decrescente",
        "Ordene os valores crescente",
        "Ordene os dados crescente",
        "Ordene os dados decrescente",
    ]

    def __init__(self, parent, task_manager):
        super(SortColumnCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso ordenar pela coluna {x}"]
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
            "name": 'order',
            "required": True,
            "position": 1,
            "patterns": [
                '(decrescente|crescente)',
                '(de maior a menor|de menor a maior)',
            ]
        })

        self.children = [
            self.dataset_name,
            self.column_name,
            self.cell_value
        ]

    def run(self, context):

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value
        cell_value = self.cell_value

        df = context[dataset_name]

        ascending = True
        if cell_value in ["decrescente", "de maior a menor"]:
            ascending= False

        try:
            df.sort_values(by=[column_name], ascending=ascending, inplace=True)
        except Exception as e:
            print(e)

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Select column from dataset")

        dataset_name = self.dataset_name.value
        column_name = self.column_name.value

        # code_generator.write("{0} = {1}['{2}']".format(context_variable, dataset_name, column_name))

