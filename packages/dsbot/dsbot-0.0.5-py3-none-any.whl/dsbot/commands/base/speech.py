import numpy as np

from .command import Command

# TODO: relative import
from dsbot.expertise.ExpertiseAnalyzer import ExpertiseAnalyzer


class Speech(Command):
    def __init__(self, config):
        self.config = config
        self.corpus = config.corpus
        self.task_manager = config.task_queue
        self.commands = config.commands
        self.bot = config.bot
        self.suggestion = config.suggestion

        # current status of the conversation
        self.status = self
        self.tag = "speech"
        self.ExpertiseAnalyzer = ExpertiseAnalyzer()

        self.children = []
        self.context = {
            'user_config':self.ExpertiseAnalyzer.user_config
        }

    def next(self, text):
        self.ExpertiseAnalyzer.analyze(text)

        #verify for cancel command intention
        wrds = self.corpus.encode(text).reshape(1, -1)
        # call the bot model to identify the tag
        results = self.bot.answer(wrds)
        max_result = np.max(results)

        # print("labels: {0}".format(self.corpus.labels))
        # print("results: {0}".format(results[0]))

        if max_result > .5:
            results_index = np.argmax(results)
            tag = self.corpus.labels[results_index]
            if tag == 'cancel_action':
                if len(self.children) > 0:
                    previous_command = self.children[-1]
                    self.children.remove(previous_command)
                    self.status = self
                    return {
                        "status": self,
                        "tag": "cancel_action",
                        "message": "Commando cancelado",
                        "context": self.context
                    }
            else:
                response = self.status.forward(text, context=self.context)
                print("User Config: {0}".format(self.ExpertiseAnalyzer.user_config))

        else:
            return {
                "status": self,
                "tag": "unknown",
                "message": "Nao entendi. Pode tentar novamente.",
                "context": self.context
            }

        # save the next status.
        self.status = response["status"]

        return response

    def propagate_text(self, text):
        for child in self.children:
            if not child.complete:
                child.propagate_text(text)

    def forward(self, text, context):
        wrds = self.corpus.encode(text).reshape(1, -1)
        # call the bot model to identify the tag
        results = self.bot.answer(wrds)
        max_result = np.max(results)

        # print("labels: {0}".format(self.corpus.labels))
        # print("results: {0}".format(results[0]))

        if max_result > .5:
            results_index = np.argmax(results)
            tag = self.corpus.labels[results_index]
            print(tag)

            # generate a new child for de speech AST
            _new_command = self.commands[tag]
            _node = _new_command(
                parent = self,
                task_manager = self.task_manager
            )
            self.children.append(_node)

            commands = self.ExpertiseAnalyzer.user_config['commands']
            self.suggestion.add(_node, commands)

            # propagate text to extract args before check for completion
            _node.propagate_text(text)
            return _node.forward(text, context)

        else:
            return {
                "status": self,
                "tag":"unknown",
                "message": "Nao entendi. Pode tentar novamente.",
                "context": self.context
            }

    # root backwards
    def backward(self, tag, text, context, **kwargs):
        result ={
            "status": self,
            "tag": tag,
            "message": text,
            "context": context,
        }
        for key in kwargs:
            result[key] = kwargs[key]
        return result

    def generate_code(self, code_generator, context):
        for child in self.children:
            child.generate_code(code_generator, context)

    def add_corpus(self, sentence, tag):
        self.corpus.add(sentence, tag)

    def print(self, level = 0):
        print("-- Speech:")
        for child in self.children:
            child.print(level=level+2)

    def report(self, message):
        print(message)
