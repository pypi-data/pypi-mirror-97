import nltk
from string import punctuation
import re

from ..utils.SpellingCheck import SpellingCheck


class DataScienceGlossary:

    def __init__(self):
        # self.language = 'english'
        self.language = 'portuguese'

        self.spelling = SpellingCheck(self.language)
        self.word_count = 0

        self.words = [
            "accuracia",
            "algoritmo",
            "presição",
            "recall",
            "f1-score",
            "outliers"
        ]

    def analyze(self, sentence, user_config):
        s_words = nltk.word_tokenize(sentence)

        # remove stopwords
        stopwords = set(nltk.corpus.stopwords.words('portuguese') + list(punctuation))
        s_words = [word for word in s_words if word not in stopwords]

        # current user input spelling caso seja entrada digitada
        corrected_input = []
        for userinput_word in s_words:
            # spell checking
            # userinput_word = self.reduce_lengthening(userinput_word)
            correct_word = self.spelling.correction(userinput_word)
            corrected_input.append(correct_word)

        # verify technical glossary
        count = user_config['text_expertise']
        old_expertise = user_config['text_expertise']
        for userinput_word in s_words:
            if userinput_word in self.words:
                count+=.0005
            else:
                self.word_count += 1
                if self.word_count % 20 == 0:
                    count -= .0001

        if count > 1:
            count = 1.0
        if count < 0:
            count = 0.0

        new_expertise = (count + old_expertise)/2

        # update user expertise
        user_config['text_expertise'] = new_expertise

    def reduce_lengthening(self, word):
        pattern = re.compile(r"(.)\1{2,}")
        return pattern.sub(r"\1\1", word)