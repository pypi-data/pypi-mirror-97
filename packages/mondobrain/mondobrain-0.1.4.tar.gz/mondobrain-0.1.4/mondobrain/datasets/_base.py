import pandas as pd
import pkg_resources

from mondobrain.core.frame import MondoDataFrame


def __load_dataset(name):
    with pkg_resources.resource_stream(__name__, f"data/{name}.csv") as stream:
        df = pd.read_csv(stream)
    return MondoDataFrame(df)


def load_bank_risk_date():
    return __load_dataset("bank-credit-risk-with-date")


def load_bronchial_risk():
    return __load_dataset("bronchial-risk")


def load_iris():
    """Return a dataframe about Irises (the flower).

    Contains the following fields:
        SepalLength          float
        SepalWidth           float
        PetalLength          float
        PetalWidth           float
        Name                 str
    """
    return __load_dataset("iris")


def load_jets():
    return __load_dataset("jets")


def load_mazda():
    return __load_dataset("mazda")


def load_political_behavior():
    return __load_dataset("political-behavior")


def load_shampoo():
    return __load_dataset("shampoo")


def load_titanic():
    return __load_dataset("titanic")
