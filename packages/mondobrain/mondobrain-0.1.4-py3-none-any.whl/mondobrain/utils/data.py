import numpy as np


def is_continuous(dtype) -> bool:
    return np.issubdtype(dtype, np.number)


def is_discrete(dtype) -> bool:
    return not is_continuous(dtype)
