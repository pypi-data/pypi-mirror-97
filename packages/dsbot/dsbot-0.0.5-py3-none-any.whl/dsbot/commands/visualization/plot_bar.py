
from ..base.command_with_args import CommandWithArgs
from ..base.argument import Argument


class BarsPlotCommand(CommandWithArgs):
    tag = "bars plot"

    patterns = [
        "Pode fazer um grafico de barras",
        "Eu quero um grafico de barras",
        "Desenha um grafico de barras com as cores",
        "Pinta um grafico de barras com as cores",
        "grafico de barras",
    ]

    def __init__(self, parent, task_manager):
        super(BarsPlotCommand, self).__init__(parent, task_manager)
        self.responses = ["Eu posso fazer um grafico de barras emtre {x} e {y}."]
        self.user_config_tag = 'visualization'

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

        self.colors = Argument({
            'parent': self,
            'name': 'colors',
            'required': False,
            'trigger': 'cores iguais a',
            'position': 1
        })

        self.children = [
            self.dataset_name,
            self.x_axis,
            self.y_axis,
            self.colors
        ]

    def run(self, context):
        import matplotlib.pyplot as plt
        plt.clf()

        dataset_name = self.dataset_name.value

        x_arg = self.x_axis.value
        x = context[dataset_name][x_arg]

        y_arg = self.y_axis.value
        y = context[dataset_name][y_arg]

        args = {
            'x': x,
            'y': y
        }

        colors_arg = self.colors.value
        if colors_arg is not None:
            colors = context[colors_arg]
            args['color'] = []
            for color in colors:
                current_color = 'blue'
                if color:
                    current_color = 'red'
                args['color'].append(current_color)

        plt.bar(**args)
        # plt.show()
        plt.savefig("plot_result.png")

        image = open("plot_result.png", 'rb')
        context["plot_result"] = image

    def generate_code(self, code_generator, context):
        code_generator.write("")
        code_generator.write("# Bar Plot ")
        code_generator.write("import matplotlib.pyplot as plt")

        x_arg = self.x_axis.value
        y_arg = self.y_axis.value
        dataset_name_arg = self.dataset_name.value

        code_generator.write("args = {")
        code_generator.indent()
        code_generator.write("'x': {0}['{1}'],".format(dataset_name_arg, x_arg))
        code_generator.write("'y': {0}['{1}']".format(dataset_name_arg, y_arg))
        code_generator.dedent()
        code_generator.write("}")

        colors_arg = self.colors.value
        if colors_arg is not None:
            colors = context[colors_arg]
            code_generator.write("args['color'] = []")
            code_generator.write("for color in {0}:".format(colors_arg))
            # For indent
            code_generator.indent()
            code_generator.write("current_color = 'blue'")
            code_generator.write("if color:")
            # If indent
            code_generator.indent()
            code_generator.write("current_color = 'red'")
            # If dedent
            code_generator.dedent()
            code_generator.write("args['color'].append(current_color)")
            # For dedent
            code_generator.dedent()

        code_generator.write("plt.bar(**args)")
        code_generator.write("plt.show()")
