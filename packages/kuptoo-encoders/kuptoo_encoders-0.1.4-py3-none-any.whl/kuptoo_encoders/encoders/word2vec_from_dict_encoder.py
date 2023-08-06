import numpy as np
from kuptoo_encoders.encoders.utils.padding import pad_2d
from kuptoo_encoders.encoders.utils.math import zeros, ones


class Word2VectorFromDictEncoder:

    def __init__(self, max_words, value2vector_dict, vector_dim, mark_pad=False, throw_exception_if_empty_vector=False,
                 debug=False):
        self.debug = debug
        self.throw_exception_if_empty_vector = throw_exception_if_empty_vector
        self.mark_pad = mark_pad
        self.max_words = max_words
        self.value2vector = value2vector_dict
        self._dim = vector_dim
        if self.mark_pad:
            self._dim += 1
        self._shape = (self.max_words, self._dim)
        self._type = "float32"

    def encode(self, data):
        if not isinstance(data, str):
            raise ValueError("Data must be str. {} {} given".format(type(data), data))

        vectors = []
        not_all_zeros = 0
        for item in data.split()[:self.max_words]:
            if item in self.value2vector:
                not_all_zeros += 1
                vector = self.value2vector[item]
                if self.mark_pad:
                    vector = np.concatenate([vector, zeros(1)])
            else:
                vector = ones(self._dim)
                if self.mark_pad:
                    vector[-1] = 0

            if len(vector) != self._dim:
                raise ValueError(
                    "Incompatible dimensions. Declared dimension --> {}!={} <-- vector from dict".format(
                        len(vector), self._dim))

            vectors.append(vector)

        if self.throw_exception_if_empty_vector and not_all_zeros == 0:
            raise ValueError(
                "Empty input. Could not find dict vectors for that sentence. inspect data \"{}\"".format(data))

        try:
            vectors = np.array(vectors)
            vectors = pad_2d(vectors, self.max_words, add_pad_class=self.mark_pad)
        except ValueError:
            vectors = zeros(self._shape)
            if self.mark_pad:
                vectors[..., -1] = 1.0

        if self.debug:
            import pprint
            words = data.split()
            pprint.pprint([(words[i] if len(words)>i else "PAD", v) for i, v in enumerate(vectors)])
        return vectors

    def shape(self):
        return self._shape

    def type(self):
        return self._type

    def dim(self):
        return self._dim
