from sklearn.preprocessing import LabelEncoder
from sklearn.utils import column_or_1d

from mondobrain.utils.data import is_continuous


def _encode_array(y):
    y = column_or_1d(y)

    if not is_continuous(y.dtype):
        raise ValueError("only able to encode numeric arrays")

    enc = LabelEncoder()
    return enc.fit_transform(y)


def encoded_mean(y):
    return _encode_array(y).mean()
