from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dropout, Dense


def build_model(vocab_size, max_len=200):
    model = Sequential()
    model.add(Embedding(vocab_size + 1, 128, input_length=max_len))
    model.add(LSTM(64, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(LSTM(64))
    model.add(Dense(1, activation="sigmoid"))

    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model
