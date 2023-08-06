import random
from .command import Command


class GreetingsCommand(Command):

    tag = "greeting"
    patterns = ["Oi", "bom dia", "olá", "tudo bem?", "como vai?", "boa tarde", "boa noite"]

    def __init__(self, parent, task_manager):
        super(GreetingsCommand, self).__init__(parent, task_manager)
        self.user_config_tag = "speaking"
        self.responses = ["Olá!", "Bom te ver de novo!", "Opa, como eu posso ajudar?"]

    def forward(self, text, context):
        user_expertise = context['user_config']['commands']
        user_expertise[self.user_config_tag] += .01
        # normalize other commands user preferences
        for key, value in user_expertise.items():
            user_expertise[key] = value / 1.01
        self.complete = True
        return self.parent.backward(self.tag, random.choice(self.responses), context)

