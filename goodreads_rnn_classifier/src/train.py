import pandas as pd
import numpy as np

from preprocessing import clean_text, genre_binarizer, is_english
from tokenizer_utils import build_vocab, save_vocab, tokenize
from model import build_model

MAX_LEN = 200


def load_data(path):
    df = pd.read_csv(path)

    df = df[df["genres"].notnull()]
    df = df[df["book_desc"].notnull()]
    df = df[df["book_desc"].str.strip().str.len() > 0]

    df["label"] = df["genres"].apply(genre_binarizer)
    df = df[df["label"].notnull()]

    df = df[df["book_desc"].apply(is_english)]

    df["clean_desc"] = df["book_desc"].apply(clean_text)

    return df.reset_index(drop=True)


def train():
    df = load_data("data/book_data_train.csv")

    vocab = build_vocab(df["clean_desc"])
    save_vocab(vocab, "models/vocab.pkl")

    X = np.stack([tokenize(t, vocab, MAX_LEN) for t in df["clean_desc"]])
    y = df["label"].values

    model = build_model(len(vocab), MAX_LEN)
    model.fit(X, y, epochs=5, batch_size=128, validation_split=0.2)

    model.save("models/model.keras")


if __name__ == "__main__":
    train()
