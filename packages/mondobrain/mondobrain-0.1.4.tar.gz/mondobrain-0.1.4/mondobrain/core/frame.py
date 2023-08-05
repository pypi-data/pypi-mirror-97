from pandas import DataFrame

from mondobrain.core.series import MondoSeries


class MondoDataFrame(DataFrame):
    """
    A MondoDataFrame object is a pandas.DataFrame that has certain
    MondoBrain specific operations and methods.

    The MondoDataFrame object is composed of 1 or more MondoSeries
    objects. The inner workings of the MondoDataFrame ensures that
    each variable is instantiated as a MondoSeries.

    For additional reference specific to the Pandas DataFrame object
    and features, please refer to the Pandas API

    **Parameters**

    data: ndarray, Iterable, dict, DataFrame, or MondoDataFrame
        Dict can contain Series, MondoSeries, arrays, constants, or list-like objects.

    **Examples**

    >>> from mondobrain.MondoDataframe import MondoDataFrame
    >>> import Pandas as pd
    >>> df = pd.read_csv('path/to/file.csv')
    >>> mdf = MondoDataFrame(df)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return MondoDataFrame

    @property
    def _constructor_sliced(self):
        return MondoSeries
