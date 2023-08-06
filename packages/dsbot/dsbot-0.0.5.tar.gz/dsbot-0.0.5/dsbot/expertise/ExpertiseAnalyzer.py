import numpy as np
import os
import pickle

from .datascience_glossary import DataScienceGlossary


class ExpertiseAnalyzer():
    def __init__(self):
        self.path = 'data/user.settings.pickle'
        self.user_config = {
            'text_expertise': 0.5,
            'commands':{
                'speaking': 0.125,
                'algorithm': 0.125,
                'preprocessing': 0.125,
                'visualization': 0.125,
                'pipe': 0.125,
                'metric': 0.125,
                'code': 0.125,
                'other': 0.125
            }
        }
        if not os.path.exists(self.path):
            with open(self.path, 'wb') as file:
                pickle.dump(self.user_config, file)
        else:
            with open(self.path, 'rb') as file:
                self.user_config = pickle.load(file)

        self.analyzers = [
            DataScienceGlossary()
        ]

    def analyze(self, sentence):
        for analyzer in self.analyzers:
            analyzer.analyze(sentence, self.user_config)

        # update user settings file
        with open(self.path, 'wb') as file:
            pickle.dump(self.user_config, file)


