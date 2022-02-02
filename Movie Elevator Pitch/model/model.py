from keras import layers
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential


class NNModel:
    def __init__(self, embedding_dim, max_words):
        self.embedding_dim = embedding_dim
        self.max_words = max_words
        self.model = Sequential()
        self.model.add(layers.Embedding(max_words, embedding_dim))
        self.model.add(layers.LSTM(175,dropout=0.2))
        self.model.add(layers.Dense(250, activation='relu'))
        self.model.add(layers.Dense(1, activation='sigmoid'))
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'], )
        self.checkpoint = ModelCheckpoint("best_model1.hdf5", monitor='val_accuracy', verbose=1, save_best_only=True,
                                      mode='auto', period=1, save_weights_only=False)

    def fit(self, X_train, y_train, X_test, y_test):
        self.model.fit(X_train, y_train, epochs=5, validation_data=(X_test,y_test), callbacks=[self.checkpoint])
        scores = self.model.evaluate(X_test, y_test)
        return scores


