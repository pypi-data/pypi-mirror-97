import os
import pickle
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


class SuggestionManager:

    def __init__(self, save_path, commands, force_training=False):
        self.path = save_path
        self.log = []

        self.possible_commands = ['None']
        for key in commands:
            self.possible_commands.append(key)
        self.y_encoder = LabelEncoder()
        self.y_encoder.fit(self.possible_commands)
        self.config = {
            "counter": 0,
            "limit": 1000,
            "data": pd.DataFrame(columns=[
                "cmd1","cmd2","cmd3","cmd4","cmd5",
                'speaking', 'algorithm', 'preprocessing',
                'visualization', 'pipe', 'metric',
                'code', 'other', 'clf'
            ])
        }

        if os.path.exists(self.path) and force_training == False:
            with open(self.path, 'rb') as file:
                self.config = pickle.load(file)
        else:
            with open(self.path, 'wb') as file:
                pickle.dump(self.config, file)

        self.model = DecisionTreeClassifier(random_state=0)
        if len(self.config['data']) > 0:
            self.train_model()

    def add(self, cmd , user_preferences):

        print(self.predict(user_preferences))

        # check for high values in the user preferences
        found = False
        for tag, value in user_preferences.items():
            if value > 0.5:
                found = True
        # check if we found a high value and there is enough  train data
        # if there is not enough train data, the line will be added as well
        if not found and self.config["counter"] > self.config["limit"]:
            # add the current command for further analysis
            self.log.append(cmd.tag)
            return

        # get the last 5 commands
        current_line = ['None', 'None', 'None', 'None', 'None']
        n = len(self.log)
        for i in range(0, min(n, 5)):
            log_index = (n-i)-1
            line_index = (5-i)-1
            current_line[line_index] = self.log[log_index]

        current_line.append(round(user_preferences["speaking"],3))
        current_line.append(round(user_preferences["algorithm"],3))
        current_line.append(round(user_preferences["preprocessing"],3))
        current_line.append(round(user_preferences["visualization"],3))
        current_line.append(round(user_preferences["pipe"],3))
        current_line.append(round(user_preferences["metric"],3))
        current_line.append(round(user_preferences["code"],3))
        current_line.append(round(user_preferences["other"],3))

        # add the classification at the end of the line
        current_line.append(cmd.tag)

        # add the current command for further analysis
        self.log.append(cmd.tag)

        # append a line to the dataset or override an old line
        data_index = self.config["counter"] % self.config["limit"]
        self.config["data"].loc[data_index] = current_line
        self.config["counter"] = self.config["counter"] +1

        # train a new suggestion model every 100 new lines
        if self.config["counter"] % 100 == 0:
            self.train_model()

        # save the suggestion file
        with open(self.path, 'wb') as file:
            pickle.dump(self.config, file)

    def train_model(self):
        data = self.config["data"]

        X = data.iloc[:,:-1]
        y = data.iloc[:,-1]

        y = self.y_encoder.transform(y)

        X['cmd1'] = self.y_encoder.transform(X['cmd1'])
        X['cmd2'] = self.y_encoder.transform(X['cmd2'])
        X['cmd3'] = self.y_encoder.transform(X['cmd3'])
        X['cmd4'] = self.y_encoder.transform(X['cmd4'])
        X['cmd5'] = self.y_encoder.transform(X['cmd5'])

        self.model.fit(X, y)

    def predict(self, user_preferences):

        if len(self.config['data']) < 10:
            return self.possible_commands[0]

        # get the last 5 commands
        current_line = ['None', 'None', 'None', 'None', 'None']
        n = len(self.log)
        for i in range(0, min(n, 5)):
            log_index = (n - i) - 1
            line_index = (5 - i) - 1
            current_line[line_index] = self.log[log_index]

        current_line = list(self.y_encoder.transform(current_line))

        current_line.append(round(user_preferences["speaking"], 3))
        current_line.append(round(user_preferences["algorithm"], 3))
        current_line.append(round(user_preferences["preprocessing"], 3))
        current_line.append(round(user_preferences["visualization"], 3))
        current_line.append(round(user_preferences["pipe"], 3))
        current_line.append(round(user_preferences["metric"], 3))
        current_line.append(round(user_preferences["code"], 3))
        current_line.append(round(user_preferences["other"], 3))

        y_pred = self.model.predict([current_line])
        command = self.y_encoder.inverse_transform(y_pred)
        return command
