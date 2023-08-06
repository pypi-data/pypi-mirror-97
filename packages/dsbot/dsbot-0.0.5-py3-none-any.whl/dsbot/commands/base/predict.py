from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class PredictCommand(CommandWithArgs):

    tag = "predict"
    patterns = [
        "queria predizer",
        "prediz usando o modelo",
        "usa o modelo para predizer"
    ]

    def __init__(self, parent, task_manager):
        super(PredictCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso usar o modelo {0} para predizer o dataset {1} e guardar o resultao em {2}."]
        self.user_config_tag = 'algorithm'

        self.complete = False

        self.dataset_name = Argument({
            'parent': self,
            'name': 'dataset_name',
            'trigger': 'dataset',
            'position': 1
        })

        self.model_name = Argument({
            'parent': self,
            'name': 'model_name',
            'trigger': 'modelo',
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
            self.model_name,
            self.context_variable
        ]

    def verify_params(self, context):
        model_name = self.model_name.value
        model = context[model_name]
        if not hasattr(model, "predict"):
            self.model_name.complete=False
            return [{
                'node': self.model_name,
                'tag': 'model_name',
                'message': '{0} nao tem um metodo predict e nao pode ser usado para predizer'.format(model_name)
            }]
        return []

    def run(self, context):
        dataset_name = self.dataset_name.value
        model_name = self.model_name.value
        context_variable = self.context_variable.value

        dataframe = context[dataset_name]
        model = context[model_name]

        # result = model.predict(dataframe.to_numpy())
        result = model.predict(dataframe)

        context[context_variable] = result

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# call algorithm predict method")

        dataset_name = self.dataset_name.value
        model_name = self.model_name.value
        context_variable = self.context_variable.value

        code_generator.write("{0} = {1}.predict({2})".format(context_variable, model_name, dataset_name))

