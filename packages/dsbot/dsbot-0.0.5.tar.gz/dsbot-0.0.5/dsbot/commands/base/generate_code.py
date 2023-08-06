from .command_with_args import CommandWithArgs
from ..base.argument import Argument


class GenerateScriptCommand(CommandWithArgs):

    tag = "generate_code"
    patterns = [
        "Gera um script",
        "Salva um arquivo com o codigo fonte",
        "Salva o meu script",
        "Gera o codigo"
    ]

    def __init__(self, parent, task_manager):
        super(GenerateScriptCommand, self).__init__(parent, task_manager)
        self.responses = ["Posso gerar o script em  {script_path}."]
        self.user_config_tag = 'code'
        self.complete = False

        self.script_path_arg = Argument({
            "parent": self,
            "name": 'script_path',
            "required": False,
            "position": 1,
            "patterns": [
                'em ([a-zA-Z0-9_.\\\/]+)',
                'no arquivo ([a-zA-Z0-9_.\\\/]+)',
                'script_path\s*=\s*([a-zA-Z0-9_.\\\/]+)'
            ]
        })

        self.children = [
            self.script_path_arg
        ]

    def run(self, context):
        script_path_arg = self.script_path_arg.value
        print("Generating script in {0}".format(script_path_arg))

        root = self
        while hasattr(root, 'parent'):
            root = root.parent

        code_generator = CodeGeneratorBackend()
        code_generator.write("if __name__ == '__main__':")
        code_generator.indent()
        # code_generator.write("print('Hello Code Generator!')")
        root.generate_code(code_generator, context)
        code = code_generator.end()

        file = open(script_path_arg, 'w')
        file.write(code)
        file.close()


class CodeGeneratorBackend:

    def __init__(self, tab="\t"):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return "".join(self.code)

    def write(self, string):
        self.code.append(self.tab * self.level + string + '\n')

    def indent(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError("internal error in code generator")
        self.level = self.level - 1