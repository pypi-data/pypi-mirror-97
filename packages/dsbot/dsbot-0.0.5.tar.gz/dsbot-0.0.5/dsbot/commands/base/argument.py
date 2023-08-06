import re
import random

from ..base.command import Command


class Argument(Command):

    tag = 'argument'

    def __init__(self, options):
        if not "parent" in options:
            raise ValueError("Commands must know its parent node")

        super(Argument, self).__init__(options["parent"], None)
        self.responses = ["Qual seria o valor de {0}"]

        self.complete = False
        self.value = None

        if not "name" in options:
            raise ValueError("Commands must have  a name")
        self.name = options["name"]

        self.trigger = None
        if "trigger" in options:
            self.trigger = options["trigger"]

        self.position = 1
        if "position" in options:
            self.position = options["position"]

        self.required = True
        if "required" in options:
            self.required = options["required"]

        if "patterns" in options:
            self.patterns = options["patterns"]
        else:
            self.patterns = [
                r'{0}\s*=\s*([a-zA-Z0-9_\(\)]+)',
            ]
            if self.trigger is not None:
                self.patterns.append("{0} ([a-zA-Z0-9_\(\)]+)".format(self.trigger))

    def propagate_text(self, text):
        self.process(text)
        if hasattr(self,'children'):
            for child in self.children:
                child.propagate_text(text)

    def forward(self, text, context):
        self.process(text)
        if self.complete:
            return self.parent.backward(None, text, context)
        else:
            return {
                "status": self,
                "tag": self.tag,
                "message": random.choice(self.responses).format(self.name),
                "context": {
                }
            }

    def process(self, text):
        for pattern in self.patterns:
            pattern_replace = pattern.format(self.name)
            match = re.search(pattern_replace, text, re.IGNORECASE)
            if match:
                self.value = match.group(self.position)

            if match or not self.required:
                self.complete = True
