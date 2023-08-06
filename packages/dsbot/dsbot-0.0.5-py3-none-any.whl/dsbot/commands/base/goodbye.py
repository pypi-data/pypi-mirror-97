import random
from .command import Command


class GoodbyeCommand(Command):

    tag = "goodbye"
    patterns = ["bye", "ate mais", "tchau", "estou indo", "adeus"]

    def __init__(self, parent, task_manager):
        super(GoodbyeCommand, self).__init__(parent, task_manager)
        self.user_config_tag = 'speaking'
        self.responses = ["Ate mais.", "A gente se fala", "Fui"]

    def forward(self, text, context):
        self.complete = True
        user_expertise = context['user_config']['commands']
        user_expertise[self.user_config_tag] += .01
        # normalize other commands user preferences
        for key, value in user_expertise.items():
            user_expertise[key] = value / 1.01
        return self.parent.backward(self.tag, random.choice(self.responses), context)


