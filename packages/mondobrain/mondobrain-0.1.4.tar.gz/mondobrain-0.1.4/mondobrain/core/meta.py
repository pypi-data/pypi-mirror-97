from enum import Enum

import mondobrain as mb
from mondobrain.core.frame import MondoDataFrame
from mondobrain.dd_transformer import DDTransformer
from mondobrain.utils import meta as meta_utils, utilities


class Direction(str, Enum):
    in_ = "in"
    out = "out"
    both = "both"


class Inverse(str, Enum):
    in_rule = "in_rule"


class BaseExploration:
    def __init__(self):
        self.result = None

    def explore(self, options: dict):
        raise NotImplementedError(".explore() must be overridden")

    def encode_options(self, mdf: MondoDataFrame, outcome: str, encoder: DDTransformer):
        pass

    def decode_results(self, edf: MondoDataFrame, outcome: str, encoder: DDTransformer):
        if self.result is not None:
            self.result["rules"] = meta_utils.decode_meta_rules(
                self.result["rules"], edf, outcome, encoder
            )


class ClassExploration(BaseExploration):
    """
    Define a MetaMondo exploration using a class-based strategy.

    Feature rules are gathered by learning on multiple classes in multiple directions.
    For discrete outcome variables, this means in or out of each outcome modality and
    for continuous outcome variables, this means min and/or max

    **Parameters**

    classes: List[str] (optional), default=None
        For discrete outcomes, a list of modalities to explore.
        For continuous outcomes, a list containing 'min' and/or 'max'.
        If None, explore all classes.

    direction: 'in', 'out', 'both' (optional), default='both'
        Direction to explore each outcome class.  Only applicable for discrete
        outcomes.

        * **in**: find feature rules inside of the outcome class
        * **out**: find feature rules outside of the outcome class
        * **both**: do both in and out
        * **None**: do not explore directions (for continuous outcome variables)

    inverse: 'in_rule' (optional), default='in_rule'
        Strategy for finding "inverse" rules when a feature rule is found

        * **in_rule**: find a rule inside the feature rule in the opposite direction
        * **None**: do not add inverse rules

    depth: int (optional), default=1
        The number of exploration cycles.

    parallel: bool (optional), default=False
        Explore each outcome class independently and in parallel.

    **Examples**

    Using the solver to run a ClassExploration

    >>> mb.api_key = "<API KEY>"
    >>> mb.api_secret = "<API SECRET>"
    >>> solver = mb.Solver()
    >>> solver.fit_meta(
    >>>     features, outcome,
    >>>     exp=ClassExploration(classes=['outcomeA'], inverse=None, depth=3)
    >>> )
    >>> solver.meta
    {
        'rules': ...list of rules found by MetaMondo...,
        'df': ...MondoDataFrame with feature rules included...
    }
    """

    def __init__(
        self,
        classes=None,
        direction=Direction.both,
        inverse=Inverse.in_rule,
        depth=1,
        parallel=False,
    ):
        super(ClassExploration, self).__init__()
        self.classes = classes
        self.direction = direction
        self.inverse = inverse
        self.depth = depth
        self.parallel = parallel

    def explore(self, options: dict):
        options.update(
            {
                "classes": self.classes,
                "direction": self.direction,
                "inverse": self.inverse,
                "depth": self.depth,
                "parallel": self.parallel,
            }
        )

        task = mb.api.meta_class_start(**options)

        self.result = mb.api.meta_result(id=task["id"])

    def encode_options(self, mdf: MondoDataFrame, outcome: str, encoder: DDTransformer):
        if mdf[outcome].var_type == "discrete" and self.classes is not None:
            self.classes = [
                utilities.encode_value(mdf, outcome, x, encoder) for x in self.classes
            ]


class ExclusionSetExploration(BaseExploration):
    """
    Define a MetaMondo exploration using an exclusion set strategy.

    Feature rules are gathered by learning a rule, then learning again on the exclusion
    set (the set of data points outside of the rule), repeating until the exclusion set
    reaches a minimum number of data points.

    **Parameters**

    min_size: int (optional), default=10
        The minimum size of the exclusion set.  Stops exploration when the
        exclusion set is below this size.

    classes: List[str] (optional), default=None
        For discrete outcomes, a list of modalities to explore.
        For continuous outcomes, a list containing 'min' and/or 'max'.
        If None, explore all classes.

    direction: 'in', 'out', 'both' (optional), default='both'
        Direction to explore each outcome class.  Only applicable for discrete
        outcomes.

        * **in**: find feature rules inside of the outcome class
        * **out**: find feature rules outside of the outcome class
        * **both**: do both in and out
        * **None**: do not explore directions (for continuous outcome variables)

    depth: int (optional), default=1
        The number of exploration cycles.

    parallel: bool (optional), default=False
        Explore each outcome class independently and in parallel.

    **Examples**

    Using the solver to run an ExclusionSetExploration

    >>> mb.api_key = "<API KEY>"
    >>> mb.api_secret = "<API SECRET>"
    >>> solver = mb.Solver()
    >>> solver.fit_meta(
    >>>     features, outcome,
    >>>     exp=ExclusionSetExploration(min_size=5, direction='in', parallel=True)
    >>> )
    >>> solver.meta
    {
        'rules': ...list of rules found by MetaMondo...,
        'df': ...MondoDataFrame with feature rules included...
    }
    """

    def __init__(
        self,
        min_size=10,
        classes=None,
        direction=Direction.both,
        depth=1,
        parallel=False,
    ):
        super(ExclusionSetExploration, self).__init__()
        self.min_size = min_size
        self.classes = classes
        self.direction = direction
        self.depth = depth
        self.parallel = parallel

    def explore(self, options: dict):
        options.update(
            {
                "min_size": self.min_size,
                "classes": self.classes,
                "direction": self.direction,
                "depth": self.depth,
                "parallel": self.parallel,
            }
        )

        task = mb.api.meta_exclusion_set_start(**options)

        self.result = mb.api.meta_result(id=task["id"])

    def encode_options(self, mdf: MondoDataFrame, outcome: str, encoder: DDTransformer):
        if mdf[outcome].var_type == "discrete" and self.classes is not None:
            self.classes = [
                utilities.encode_value(mdf, outcome, x, encoder) for x in self.classes
            ]
