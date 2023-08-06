
import pickle
import nltk
import re
import numpy as np
from sentence_transformers import SentenceTransformer

class BERTCorpus:

    def __init__(self, save_path, commands, verbose, force_training=False):
        self.verbose = verbose
        self.save_path = save_path
        self.commands = commands
        self.bert_model = SentenceTransformer('distiluse-base-multilingual-cased')

        if force_training:
            self.load_corpus()
        else:
            try:
                with open(self.save_path, "rb") as f:
                    self.labels, self.training, self.output = pickle.load(f)
            except:
                self.load_corpus()

    def load_corpus(self):

        labels = []
        tags=[]
        training = []
        output = []

        # for intent in data["intents"]:
        for key, command in self.commands.items():
            for pattern in command.patterns:
                bert_sentences_embeddings = list(self.bert_model.encode(pattern))
                tags.append(command.tag)
                training.append(bert_sentences_embeddings)

            if command.tag not in labels:
                labels.append(command.tag)

        labels = sorted(labels)
        out_empty = [0 for _ in range(len(labels))]
        for tag in tags:
            output_row = out_empty[:]
            output_row[labels.index(tag)] = 1
            output.append(output_row)

        self.labels = labels
        self.training = np.array(training)
        self.output = np.array(output)

        with open(self.save_path, "wb") as f:
            pickle.dump((self.labels, self.training, self.output), f)

    def encode(self, sentence):
        return self.bert_model.encode([sentence])

    def add(self, sentence, tag):
        try:
            # read the dataset
            with open(self.save_path, "rb") as f:
                self.labels, self.training, self.output = pickle.load(f)
                x = self.bert_model.encode([sentence])

                # find the phrase in the dataset
                if x in self.training:
                    return

                y = [0 for _ in range(len(self.labels))]
                y[self.labels.index(tag)] = 1

                self.training.append(x)
                self.output.append(y)
            # add the current phrase to the dataset
            with open(self.save_path, "wb") as f:
                pickle.dump((self.labels, self.training, self.output), f)
        except Exception as e:
            print(e)
