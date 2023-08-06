import numpy as np

from .utils.BotConfig import BotConfig
from .commands.base.speech import Speech


class DSBot:

    def __init__(self, **kwargs):
        self.initial_config = kwargs
        self.config = BotConfig(**self.initial_config)
        self.speech_manager = Speech(self.config)
        self.bot = self.config.bot
        self.corpus = self.config.corpus
        self.commands = self.config.commands

    def start(self):
        print("Começe a falar com o bot!")

        while True:
            # print("Escutando ...")
            text = self.config.input()

            # case input control did not undestand
            if not text:
                print("Bot: Nao entendi. Pode tentar novamente.")
                continue

            print("You: {0}".format(text))

            response = self.speech_manager.next(text)

            tag = response["tag"]
            message = response["message"]

            print("Bot: {0}".format(response))

            # exit the while loop
            if tag == 'goodbye':
                self.speech_manager.print()
                # break

        print("Done!")

    def test(self):
        print("Running initial test set ...")

        testing_set = {
            "asfasdf": "unknown",
            "lnvr": "unknown",
            "ewetrt": "unknown",
            "asdfww": "unknown",
            "Vamos carregar o dataset outliers_sample_data em data/outliers.csv": "load_dataset",
            "Selecciona a coluna target e guarda em outliers_target": "column_extract",
            "Remove a coluna target do dataset outliers_sample_data": "column_deletion",
            "Roda o algoritmo loda e guarda em autoencoder_model": "algorithm",
            "Vamos a predizer usando o modelo autoencoder_model e guarda em model_predictions": "predict",
            "Desenha um grafico de pontos com as cores iguais a model_predictions": "scatter plot",
            "Salva o codigo em data/sample.py": "generate_code",
            "Formatar os dados da coluna x1 do dataset cleaning_sample_data para letra minuscula": "lower_upper_case",
            "ordene os dados da coluna x1 do dataset cleaning_sample_data de maneira crescente": "sort_column"
        }

        for key, command in self.commands.items():
            for pattern in command.patterns:
                testing_set[pattern] = command.tag

        total_tests = len(testing_set)

        correct_threshold_5 = 0
        wrong_cases_5 = []

        correct_threshold_6 = 0
        wrong_cases_6 = []

        correct_threshold_7 = 0
        wrong_cases_7 = []

        for pattern, tag in testing_set.items():
            wrds = self.corpus.encode(pattern).reshape(1, -1)
            results = self.bot.answer(wrds)
            max_result = np.max(results)

            results_index = np.argmax(results)
            predicted_tag = self.corpus.labels[results_index]

            if max_result > .5:
                if predicted_tag == tag:
                    correct_threshold_5 += 1
                else:
                    wrong_cases_5.append(pattern)
            else:
                if 'unknown' == tag:
                    correct_threshold_5 += 1
                else:
                    wrong_cases_5.append(pattern)

            if max_result > .6:
                if predicted_tag == tag:
                    correct_threshold_6 += 1
                else:
                    wrong_cases_6.append(pattern)
            else:
                if 'unknown' == tag:
                    correct_threshold_6 += 1
                else:
                    wrong_cases_6.append(pattern)

            if max_result > .7:
                if predicted_tag == tag:
                    correct_threshold_7 += 1
                else:
                    wrong_cases_7.append(pattern)
            else:
                if 'unknown' == tag:
                    correct_threshold_7 += 1
                else:
                    wrong_cases_7.append(pattern)

        print("threshold 0.5 : {0}/{1}".format(correct_threshold_5, total_tests))
        print("threshold 0.6 : {0}/{1}".format(correct_threshold_6, total_tests))
        print("threshold 0.7 : {0}/{1}".format(correct_threshold_7, total_tests))

        print("Failed 0.5: {0}".format(wrong_cases_5))
        print("Failed 0.6: {0}".format(wrong_cases_6))
        print("Failed 0.7: {0}".format(wrong_cases_7))

    def register(self, cmd):
        # add command to the config
        if 'commands' not in self.initial_config:
            self.initial_config['commands'] = self.config.commands
        self.initial_config['commands'][cmd.tag] = cmd

    def train(self):
        old_force_training = self.config.force_training
        self.initial_config['force_training']= True

        self.config = BotConfig(**self.initial_config)
        self.speech_manager = Speech(self.config)
        self.bot = self.config.bot
        self.corpus = self.config.corpus
        self.commands = self.config.commands

        self.config.force_training = old_force_training

