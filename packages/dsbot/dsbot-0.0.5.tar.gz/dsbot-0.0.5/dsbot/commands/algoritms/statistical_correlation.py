from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class StatisticalCorrelationCommand(CommandWithArgs):

    tag = "statistical_correlation"
    patterns = [
        "pode fazer uma correlação estatistica",
        "correlação estatistica",
        "faz uma correlação estatistica"
    ]

    def __init__(self, parent, task_manager):
        super(StatisticalCorrelationCommand, self).__init__(parent, task_manager)
        self.responses = ["Eu posso fazer uma correlação estatistica emtre {x} e {y}."]
        self.user_config_tag = 'preprocessing'
        self.dataset_name = Argument({
            'parent': self,
            'name': 'dataset_name',
            'trigger': 'dataset',
            'position': 1
        })

        self.x_axis = Argument({
            'parent': self,
            'name': 'x',
            'trigger': 'eixo x igual a',
            'position': 1
        })

        self.y_axis = Argument({
            'parent': self,
            'name': 'y',
            'trigger': 'eixo y igual a',
            'position': 1
        })

        self.children = [
            self.dataset_name,
            self.x_axis,
            self.y_axis,
        ]

    def run(self, context):
        from scipy import stats

        dataset_name = self.dataset_name.value

        x_arg = self.x_axis.value
        x = context[dataset_name][x_arg]

        y_arg = self.y_axis.value
        y = context[dataset_name][y_arg]

        result = stats.pearsonr(x, y)
        print(result)

    def generate_code(self, code_generator, context):

        code_generator.write("")
        code_generator.write("# Pearson Statistical Correlation ")
        code_generator.write("from scipy import stats")

        x_arg = self.x_axis.value
        x_arg_name = self.x_axis.name

        y_arg = self.y_axis.value
        y_arg_name = self.y_axis.name

        dataset_name_arg = self.dataset_name.value

        code_generator.write("{0} = {1}['{2}']".format(x_arg_name, dataset_name_arg, x_arg))
        code_generator.write("{0} = {1}['{2}']".format(y_arg_name, dataset_name_arg, y_arg))
        code_generator.write("result = stats.pearsonr({0}, {1})".format(x_arg_name, y_arg_name))
        code_generator.write("print(result)")