import random
from .command import Command


class SuggestCommand(Command):

    tag = "suggest"
    patterns = [
        "O que eu faço agora",
        "Como posso continuar",
        "Me ajuda aqui",
        "O que geralmente feito nesta situaçao"
    ]

    def __init__(self, parent, task_manager):
        super(SuggestCommand, self).__init__(parent, task_manager)
        self.user_config_tag = "speaking"
        self.responses = ["Suggestion :{0}!"]

    def forward(self, text, context):

        # Update user expertise
        user_expertise = context['user_config']['commands']
        user_expertise[self.user_config_tag] += .01
        # normalize other commands user preferences
        for key, value in user_expertise.items():
            user_expertise[key] = value / 1.01
        self.complete = True

        return self.parent.backward(self.tag, random.choice(self.responses), context)

