
import pickle
import nltk
import re
import numpy as np
from string import punctuation

# English
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.rslp import RSLPStemmer


class BagOfWordsCorpus:

    def __init__(self, save_path, commands, verbose, force_training=False):
        self.verbose = verbose
        self.save_path = save_path

        # English
        # self.stemmer = LancasterStemmer()
        # Portuguese
        self.stemmer = RSLPStemmer()

        self.stopwords = set(nltk.corpus.stopwords.words('portuguese') + list(punctuation))

        self.commands = commands

        if force_training:
            self.load_corpus()
        else:
            try:
                with open(save_path, "rb") as f:
                    self.words, self.labels, self.training, self.output = pickle.load(f)
            except:
                self.load_corpus()

    def load_corpus(self):

        words = []
        labels = []
        docs_x = []
        docs_y = []

        # for intent in data["intents"]:
        for key, command in self.commands.items():
            for pattern in command.patterns:

                wrds = nltk.word_tokenize(pattern)
                wrds = [word for word in wrds if word not in self.stopwords]
                wrds = [self.stemmer.stem(w.lower()) for w in wrds]

                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(command.tag)

            if command.tag not in labels:
                labels.append(command.tag)

        words = sorted(list(set(words)))
        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, wrds in enumerate(docs_x):
            bag = []

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = np.array(training)
        output = np.array(output)

        self.words = words
        self.labels = labels
        self.training = training
        self.output = output

        with open("data/data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)

    def encode(self, sentence):
        bag = [0 for _ in range(len(self.words))]

        wrds = nltk.word_tokenize(sentence)
        wrds = [word for word in wrds if word not in self.stopwords]
        wrds = [self.stemmer.stem(w.lower()) for w in wrds]

        corrected_input = wrds

        # corrent user input spelling caso seja entrada digitada
        # corrected_input = []
        # for userinput_word in s_words:
        #     # spell checking
        #     # userinput_word = reduce_lengthening(userinput_word)
        #     correct_word = spelling.correction(userinput_word)
        #     corrected_input.append(correct_word)

        if self.verbose:
            print("Mensagem do usuario corregida para: {0}".format(corrected_input))

        for se in wrds:
            for i, w in enumerate(self.words):
                if w == se:
                    bag[i] = 1

        return np.array(bag)

    def reduce_lengthening(self, word):
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", word)

    def add(self, sentence, tag):
        try:
            # read the dataset
            with open(self.save_path, "rb") as f:
                self.labels, self.training, self.output = pickle.load(f)
                x = self.encode([sentence])

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