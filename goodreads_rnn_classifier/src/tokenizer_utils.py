import pickle
import numpy as np


def build_vocab(texts):
    vocab = set()
    for text in texts:
        for word in text.split():
            vocab.add(word)
    return {word: idx + 1 for idx, word in enumerate(vocab)}


def save_vocab(vocab, path):
    with open(path, "wb") as f:
        pickle.dump(vocab, f)


def load_vocab(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def tokenize(text, vocab, max_len=200):
    tokens = [vocab.get(word, 0) for word in text.split()]

    if len(tokens) < max_len:
        tokens = [0] * (max_len - len(tokens)) + tokens
    else:
        tokens = tokens[:max_len]

    return np.array(tokens)
