import tensorflow as tf
print(tf.__version__)


class Dense128NetBot:

    def __init__(self, model_path, corpus="", verbose=True, force_training=False):
        self.verbose = verbose
        self.model_path = model_path
        self.corpus = corpus

        if force_training:
            self.load_model()
        else:
            try:
                if self.verbose:
                    print("Procurando um modelo treinado ...")
                self.model = tf.keras.models.load_model(model_path)
            except:
                if self.verbose:
                    print("Nao foi possivel encontrar um modelo treinado. Treinando um modelo novo ...")
                    print("Amostras de treinamento: {0}".format(len(self.corpus.training[0])))
                self.load_model()

    def load_model(self):

        self.model = tf.keras.models.Sequential([
            tf.keras.layers.InputLayer(input_shape=(len(self.corpus.training[0]),)),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(128),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(32),
            # tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(len(self.corpus.output[0]), activation='softmax')
        ])

        self.model.compile(
            optimizer=tf.keras.optimizers.SGD(),
            loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
            metrics=['accuracy']
        )

        self.model.fit(self.corpus.training, self.corpus.output, epochs=1000, batch_size=16, verbose=0)

        self.model.save(self.model_path)

    def answer(self, user_speech):
        return self.model.predict(user_speech)
