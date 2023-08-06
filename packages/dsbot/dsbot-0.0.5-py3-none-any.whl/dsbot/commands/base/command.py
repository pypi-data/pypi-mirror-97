import random


class Command:

    def __init__(self, parent, task_manager):
        self.parent = parent
        self.task_manager = task_manager
        self.text = ""
        self.responses = ["Empty"]
        self.context_set = ""
        self.complete = True

    def print(self, level):
        _level = ""
        for _ in range(0,level):
            _level += ' '

        print("{0}-- {1}: {2}".format(
            _level,
            self.tag.capitalize(),
            self.text
        ))

        if hasattr(self,'children'):
            for child in self.children:
                child.print(level=level+2)

    def run(self, context):
        pass

    def verify_params(self, context):
        return []

    def propagate_text(self, text):
        if hasattr(self,'children'):
            for child in self.children:
                child.propagate_text(text)

    def generate_code(self, code_generator, context):
        if hasattr(self, 'children'):
            for child in self.children:
                child.generate_code(code_generator, context)

    def report(self, message):
        self.parent.report(message)