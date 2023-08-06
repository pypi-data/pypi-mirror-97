import speech_recognition as sr

class Microphone:
    def __init__(self, verbose=True):
        self.verbose = verbose

    def __call__(self, *args, **kwargs):
        return self.input()

    def input(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)

        try:
            # for testing purposes, we're just using the default API key
            text = r.recognize_google(audio, language="pt-BR")

            # to use another API key, use `
            # r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")

            if self.verbose:
                print("Google Speech Recognition acha que vc falou:" + text)

            return text

        except sr.UnknownValueError:
            if self.verbose:
                print("Google Speech Recognition nao entendeu a mensagem")
            return False

        except sr.RequestError as e:
            if self.verbose:
                print("Nao foi possivel conectar com Google Speech Recognition; {0}".format(e))
            return False
