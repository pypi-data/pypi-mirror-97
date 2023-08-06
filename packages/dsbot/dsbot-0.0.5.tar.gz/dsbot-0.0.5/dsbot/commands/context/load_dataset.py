import random
from sklearn import datasets

from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class LoadDatasetCommand(CommandWithArgs):

    tag = "load_dataset"
    patterns = [
        "Quero carregar um dataset",
        "Quero carregar o dataset",
        "utilizar o dataset"
    ]

    def __init__(self, parent, task_manager):
        super(LoadDatasetCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso carregar o dataset {dataset_name}."]
        self.user_config_tag = 'preprocessing'

        self.default_datasets={
            'iris': (datasets.load_iris, "datasets.load_iris()"),
            'digits':(datasets.load_digits, "datasets.load_digits()"),
            'wine':(datasets.load_wine, "datasets.load_wine()"),
            # 'airline':(sktime.datasets.load_airline, "datasets.load_airline()"),
            # 'arrow':(sktime.datasets.load_arrow_head, "datasets.load_arrow_head(return_X_y=True)"),
        }

        self.complete = False

        self.dataset_name_arg = Argument({
            "parent": self,
            "name": 'dataset_name',
            "position": 1,
            "patterns": [
                'dataset ([a-zA-Z0-9_]+)',
                'dataset_name\s*=\s*([a-zA-Z0-9_]+)'
            ]
        })

        self.dataset_path_arg = Argument({
            "parent": self,
            "name": 'dataset_path',
            "required": False,
            "position": 1,
            "patterns": [
                'em ([a-zA-Z0-9_.\\\/]+)',
                'no arquivo ([a-zA-Z0-9_.\\\/]+)',
                'dataset_path\s*=\s*([a-zA-Z0-9_.\\\/]+)'
            ]
        })

        self.children = [
            self.dataset_name_arg,
            self.dataset_path_arg
        ]

    def forward(self, text, context):
        if not self.dataset_name_arg.complete:
            return self.dataset_name_arg.forward(text, context)

        dataset_name = self.dataset_name_arg.value

        if dataset_name not in self.default_datasets:
            if not self.dataset_path_arg.complete:
                return self.dataset_path_arg.forward(text, context)

        self.complete = True

        # self.run(context)
        self.task_manager.add_task({
            'fn': self.run,
            'args': {
                'context': context,
            }
        })

        response = random.choice(self.responses)
        return self.parent.backward(self.tag, response, context)

    def run(self, context):
        dataset_name = self.dataset_name_arg.value

        if dataset_name in self.default_datasets:
            dataframe = self.load_defaults(dataset_name)
            print(dataframe)
            context[dataset_name] = dataframe

        else:
            import pandas as pd
            dataset_path = self.dataset_path_arg.value
            dataframe = pd.read_csv(dataset_path)
            context[dataset_name] = dataframe

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Load Dataset")
        code_generator.write("from sklearn import datasets")
        code_generator.write("import pandas as pd")
        code_generator.write("import numpy as np")

        dataset_name = self.dataset_name_arg.value
        if dataset_name in self.default_datasets:
            _, load_fn_code = self.default_datasets[dataset_name]
            code_generator.write("dataset = {0}".format(load_fn_code))
            code_generator.write("{0} = pd.DataFrame(".format(dataset_name))
            code_generator.indent()
            code_generator.write("data=np.c_[dataset['data'], dataset['target']],")
            code_generator.write(
                "columns= [column_name.replace(' ','') for column_name in dataset['feature_names']] + ['target']")
            code_generator.dedent()
            code_generator.write(")")
        else:
            dataset_path = self.dataset_path_arg.value
            code_generator.write("{0} = pd.read_csv('{1}')".format(dataset_name,dataset_path))

    def load_defaults(self, name):

        import pandas as pd
        import numpy as np

        load_fn , _ = self.default_datasets[name]

        dataset = load_fn()
        if type(dataset) is pd.DataFrame:
            return dataset
        else:
            return pd.DataFrame(
                data=np.c_[dataset['data'], dataset['target']],
                columns= [column_name.replace(" ","") for column_name in dataset['feature_names']] + ['target']
            )
