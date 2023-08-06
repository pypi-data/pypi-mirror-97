import os
import nltk
import ssl

from ..commands import commands
from ..corpus import BagOfWordsCorpus, BERTCorpus
from ..bots import DenseNetBot, Dense128NetBot
from ..inputs import Text

from .SuggestionManager import SuggestionManager
from .TaskQueue import TaskQueue
# from .IOC import IOC
# IOC.__version__ = "0.1.1"


class BotConfig:

    def __init__(self, **kwargs):
        self.save_path= 'data/'
        if 'save_path' in kwargs:
            self.save_path = kwargs['save_path']

        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        # verify nltk packages
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download("stopwords")

        # self.force_training = True
        self.force_training = False
        if 'force_training' in kwargs:
            self.force_training = kwargs['force_training']

        # Commands
        self.commands = commands

        # Add extension commands
        if 'extensions' in kwargs:
            for cmd in kwargs['extensions']:
                self.commands[cmd.tag] = cmd

        # replace commnds with new registered commands
        if 'commands' in kwargs:
            self.commands = kwargs['commands']

        # Corpus
        self.corpus_save_path = "{0}corpus.pickle".format(self.save_path)
        self.corpus = BagOfWordsCorpus(self.corpus_save_path, commands, verbose = False, force_training=self.force_training)
        # self.corpus = BERTCorpus(self.corpus_save_path, commands, verbose = False, force_training=self.force_training)
        if 'corpus' in kwargs:
            self.corpus = kwargs['corpus']

        # Intention bot
        self.bot_save_path = "{0}intention.bot.pickle".format(self.save_path)
        # self.bot = DenseNetBot(self.bot_save_path, self.corpus, verbose = False, force_training=self.force_training)
        self.bot = Dense128NetBot(self.bot_save_path, self.corpus, verbose = False, force_training=self.force_training)
        if 'bot' in kwargs:
            self.bot = kwargs['bot']

        # Suggestion model
        self.suggestion_save_path = "{0}suggest.corpus.pickle".format(self.save_path)
        self.suggestion = SuggestionManager(self.suggestion_save_path, commands, force_training=self.force_training)
        if 'suggestion' in kwargs:
            self.suggestion = kwargs['suggestion']

        # TaskQueue
        self.task_queue = TaskQueue(num_workers=1)
        if 'task_queue' in kwargs:
            self.task_queue = kwargs['task_queue']

        # Input
        # self.input = Microphone(verbose=False)
        self.input = Text(verbose=False)
        if 'input' in kwargs:
            self.input = kwargs['input']