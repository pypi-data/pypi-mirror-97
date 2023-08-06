
class Text:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def input(self):
        return input()

    def __call__(self, *args, **kwargs):
        return self.input()
