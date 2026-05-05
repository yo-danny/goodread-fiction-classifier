import numpy as np
from keras.models import load_model

from preprocessing import clean_text
from tokenizer_utils import load_vocab, tokenize


class Predictor:
    def __init__(self):
        self.model = load_model("models/model.keras")
        self.vocab = load_vocab("models/vocab.pkl")
        self.max_len = 200

    def predict_from_text(self, text):
        text = clean_text(text)
        tokens = tokenize(text, self.vocab, self.max_len)
        tokens = np.expand_dims(tokens, axis=0)

        prob = self.model.predict(tokens)[0][0]

        return {
            "prediction": "fiction" if prob > 0.5 else "non-fiction",
            "probability": float(prob),
        }
