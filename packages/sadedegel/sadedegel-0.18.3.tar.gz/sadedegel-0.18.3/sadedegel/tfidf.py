from typing import List
import numpy as np

from .bblock.vocabulary import Vocabulary


class BinaryTF:
    def __init__(self, vocabulary: Vocabulary):
        self.vocabulary = vocabulary

    def __call__(self, tokens: List[str]):
        v = np.zeros(len(self.vocabulary))

        for token in tokens:
            t = self.vocabulary[token]
            if not t.is_oov:
                v[t.id] = 1

        return v


class RawTF:
    def __init__(self, vocabulary: Vocabulary):
        self.vocabulary = vocabulary

    def __call__(self, tokens: List[str]):
        v = np.zeros(len(self.vocabulary))

        for token in tokens:
            t = self.vocabulary[token]
            if not t.is_oov:
                v[t.id] += 1

        return v

# def get_tf_vectorizer_by_name(name: str, vocabulary: Vocabulary):
#     if name is None:
#         name = configuration['tf']
#
#     if name == "binary":
#         pass
#     elif name == "raw":
#         pass
#     elif name == "freq":
#         pass
#     elif name == "log_norm":
#         pass
#     elif name == "double_norm":
#         pass
#     else:
#         warnings.warn(f"Unknown tf method {name}. Failing back to binary tf", UserWarning)
#
#         return BinaryTF(vocabulary)
#
#
# def get_idf_vectorizer_by_name(name: str):
#     pass
