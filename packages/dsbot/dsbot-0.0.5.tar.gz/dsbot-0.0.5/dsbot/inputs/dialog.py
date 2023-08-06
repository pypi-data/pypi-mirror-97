

class Dialog:
    def __init__(self, dialog = [], verbose=True):
        self.dialog = dialog
        self.index = -1
        self.verbose = verbose

    def input(self):
        self.index += 1
        try:
            return self.dialog[self.index]
        except Exception as e:
            return input()

    def __call__(self, *args, **kwargs):
        return self.input()
