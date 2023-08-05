from numpy import issubdtype, number
from pandas import Series

from mondobrain.error import InvalidTargetError


class MondoSeries(Series):
    """
    A MondoSeries object is a pandas.Series that has certain
    MondoBrain specific operations and methods.

    **Parameters**

    data: array-like, Iterable, dict, or scalar value
        Contains data stored in Series.

    **Attributes**

    target_class: str (optional for feature variables)
        If the MondoSeries is passed to the prescriber.Solver object as
        a target variable, a target_class must be defined for the
        MondoBrain Solver to optimize with.

        Discrete variables: label set from the set prescriber.Solver.classes
        Continous variables: "max" or "min"

    classes: numpy.array (read only)
        A list of class labels or modalities known to the MondoSeries.

    case_point: numeric (optional)
        Scalar value of type int or float that can be set for continuous
        variables. Case point ensures that a rule is found with the Solver
        that contains the referenced point.

    var_type: str (read only)
        Label that identifies the variable as "discrete" for categorical values
        and "continuous" for numeric values.

    **Examples**

    >>> from mondobrain.MondoSeries import MondoSeries
    >>> import Numpy as np
    >>> arr = np.arange(100)
    >>> ms = MondoSeries(arr, name='some_variable')
    >>> ms.target_class = 'some_class'

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_point = None
        self.target_class = None

    @property
    def _constructor(self):
        return MondoSeries

    @property
    def target_class(self):
        return self._target_class

    @target_class.setter
    def target_class(self, value):
        if value is None:
            self._target_class = None

        elif self.var_type == "discrete":
            if value in self.classes:
                self._target_class = value
            else:
                raise InvalidTargetError(
                    f'"{value}" is not a modality of the variable "{self.name}"'
                )

        else:
            if value in ["max", "min"]:
                self._target_class = value
            else:
                raise InvalidTargetError(
                    f'Outcome target must be either "max" or "min" '
                    f'for the continuous variable "{self.name}"'
                )

    @property
    def classes(self):
        return self.unique()

    @classes.setter
    def classes(self, value):
        raise TypeError("'target_class' attribute does not support assignment")

    @property
    def case_point(self):
        return self._case_point

    @case_point.setter
    def case_point(self, value):
        self._case_point = value

    @property
    def var_type(self):
        _var_type = None
        if issubdtype(self.dtype, number):
            _var_type = "continuous"
        else:
            _var_type = "discrete"
        return _var_type
