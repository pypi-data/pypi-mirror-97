from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class AccuracyCommand(CommandWithArgs):

    tag = "metrics_accuracy"
    patterns = [
        "calcula a acuracia",
        "accuracia",
        "qual foi a acuracia",
    ]

    def __init__(self, parent, task_manager):
        super(AccuracyCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso calcular a acuracia e guardar em {0}."]
        self.user_config_tag = 'metric'

        self.complete = False

        self.y_true_arg = Argument({
            'parent': self,
            'name': 'y_true',
            'trigger': 'y_true',
            'position': 1
        })

        self.y_pred_arg = Argument({
            'parent': self,
            'name': 'y_pred',
            'trigger': 'y_pred',
            'position': 1
        })

        self.context_variable = Argument({
            'parent': self,
            'name': 'variable_name',
            'trigger': 'guarda em',
            'position': 1
        })

        self.children = [
            self.y_true_arg,
            self.y_pred_arg,
            self.context_variable
        ]

    def run(self, context):

        y_true_arg = self.y_true_arg.value
        y_pred_arg = self.y_pred_arg.value
        context_variable = self.context_variable.value

        y_true = context[y_true_arg]
        y_pred = context[y_pred_arg]

        from sklearn.metrics import accuracy_score
        result = accuracy_score(y_true, y_pred)
        context[context_variable] = result

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Accuracy Score")

        y_true_arg = self.y_true_arg.value
        y_pred_arg = self.y_pred_arg.value
        context_variable = self.context_variable.value

        code_generator.write("from sklearn.metrics import accuracy_score")
        code_generator.write("{0} = accuracy_score({1}, {2})".format(context_variable, y_true_arg, y_pred_arg))

