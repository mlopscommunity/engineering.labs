import numpy as np
from nltk.tokenize.treebank import TreebankWordTokenizer

from config import (
    REMOVE_DICT,
    ISOLATE_DICT,
)

TOKENIZER = TreebankWordTokenizer()


def handle_symbols(x):
    x = x.translate(REMOVE_DICT)
    x = x.translate(ISOLATE_DICT)
    return x


def handle_contractions(x):
    x = TOKENIZER.tokenize(x)
    return x


def fix_quote(x):
    x = [x_[1:] if x_.startswith("'") else x_ for x_ in x]
    x = ' '.join(x)
    return x


def preprocess(x):
    # 1. Remove all symbols in the corpus that do not appear in the embeddings.
    x = handle_symbols(x)
    # 2. Handle contractions using the TreebankTokenizer.
    x = handle_contractions(x)
    # 3. Remove the apostrophe symbol at the beginning of the token words.
    x = fix_quote(x)
    return x


def build_matrix(word_index, glove_model, max_featrs):
    embedding_matrix = np.zeros((max_featrs + 1, 300))
    unknown_words = []

    for word, i in word_index.items():
        if i <= max_featrs:
            try:
                embedding_matrix[i] = glove_model[word]
            except KeyError:
                try:
                    embedding_matrix[i] = glove_model[word.lower()]
                except KeyError:
                    try:
                        embedding_matrix[i] = glove_model[word.title()]
                    except KeyError:
                        unknown_words.append(word)
    return embedding_matrix, unknown_words
