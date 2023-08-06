import numpy as np
from kuptoo_encoders.encoders.utils.math import zeros


def get_pad_vector(shape):
    vec = zeros(shape)
    vec[..., -1] = 1.0
    return vec


def pad_2d(result, vsize, add_pad_class=True):
    result = np.array(result)
    result = result[:vsize, ...]
    pad = vsize - len(result)
    if pad > 0:
        if pad == vsize:
            raise ValueError("Empty encoded text.")
        result = np.pad(result, [[0, pad, ], [0, 0]], mode='constant')
        if add_pad_class:
            result[-pad:, -1] = 1.0
    return result


def pad_3d(vector, length, dim):
    result_length = len(vector)

    pad_with = length - result_length

    if result_length == 0:
        vector = get_pad_vector((length, dim))
    elif pad_with > 0:
        vector = np.array(vector)  # batch of vectors
        if type(dim) == int:
            dim = [dim]
        elif type(dim) == tuple:
            dim = list(dim)
        padded = get_pad_vector(tuple([pad_with] + dim))
        vector = np.vstack((vector, padded))
    else:
        vector = np.array(vector[0:length])

    return vector
