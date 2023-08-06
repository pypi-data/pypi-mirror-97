import random
from .command import Command


class CancelCommand(Command):

    tag = "cancel_action"
    patterns = [
        "Para esse comando",
        "Cancela esse comando",
        "Cancela o comando anterior"
    ]

    def __init__(self, parent, task_manager):
        super(CancelCommand, self).__init__(parent, task_manager)
        self.user_config_tag = "other"
        self.responses = ["Cancelado o commando anterior"]

    def forward(self, text, context):

        # Update user expertise
        user_expertise = context['user_config']['commands']
        user_expertise[self.user_config_tag] += .01
        # normalize other commands user preferences
        for key, value in user_expertise.items():
            user_expertise[key] = value / 1.01
        self.complete = True

        return self.parent.backward(self.tag, random.choice(self.responses), context)





