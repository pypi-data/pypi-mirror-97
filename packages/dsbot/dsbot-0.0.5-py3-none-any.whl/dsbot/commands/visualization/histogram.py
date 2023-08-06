from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class HistogramCommand(CommandWithArgs):

    tag = "histogram"
    patterns = [
        "Pode fazer um histograma",
        "Eu quero um histograma",
        "Desenha um histograma",
        "faz um histograma",
        "histograma",
    ]

    def __init__(self, parent, task_manager):
        super(HistogramCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso fazer um histograma com {x}."]
        self.user_config_tag = 'visualization'

        self.complete = False

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

        self.children = [
            self.dataset_name,
            self.x_axis
        ]

    def run(self, context):
        import matplotlib.pyplot as plt
        plt.clf()

        dataset_name = self.dataset_name.value
        x_arg = self.x_axis.value
        x = context[dataset_name][x_arg]

        plt.hist(x, bins=10)
        # plt.show()
        plt.savefig("plot_result.png")

        image = open("plot_result.png", 'rb')
        context["plot_result"] = image

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Histogram ")
        code_generator.write("import matplotlib.pyplot as plt")

        dataset_name = self.dataset_name.value
        x_arg = self.x_axis.value
        x_arg_name = self.x_axis.name

        code_generator.write("{0} = {1}['{2}']".format(x_arg_name, dataset_name, x_arg))
        code_generator.write("plt.hist({0}, bins=10)".format(x_arg_name))
        code_generator.write("plt.show()")

