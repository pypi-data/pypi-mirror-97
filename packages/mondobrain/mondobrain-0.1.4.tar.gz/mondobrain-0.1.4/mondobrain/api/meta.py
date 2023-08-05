from typing import Dict, List, Union

from mondobrain.core.meta import Direction, Inverse

from .requestor import APIRequestor


def meta_class_start(
    outcome: str = None,
    timeout: int = None,
    min_size_frac: float = None,
    # case_points: dict = None, DISABLED FOR NOW
    classes: List[str] = None,
    direction: Direction = Direction.both,
    encode: List[str] = None,
    inverse: Inverse = None,
    depth: int = None,
    parallel: bool = False,
    data: List[Dict[str, Union[None, str, int, float]]] = None,
    **kwargs
):
    """
    Start a MetaMondo exploration using a class-based strategy.

    Feature rules are gathered by learning on multiple classes in multiple directions.
    For discrete outcome variables, this means in or out of each outcome modality and
    for continuous outcome variables, this means min and/or max

    Parameters
    ----------
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

    inverse: 'in_rule' (optional), default=None
        Strategy for finding "inverse" rules when a feature rule is found

        * **in_rule**: find a rule inside the feature rule in the opposite direction
        * **None**: do not add inverse rules

    depth: int (optional), default=1
        The number of exploration cycles.

    parallel: bool (optional), default=False
        Explore each outcome class independently and in parallel.

    outcome: str
        See **api.solve_start**

    data: List[dict]
        See **api.solve_start**

    timeout: int (optional)
        See **api.solve_start**

    min_size_frac: float (optional)
        See **api.solve_start**
    """
    params = {
        "outcome": outcome,
        "timeout": timeout,
        "min_size_frac": min_size_frac,
        "classes": classes,
        "direction": direction,
        "encode": encode,
        "inverse": inverse,
        "depth": depth,
        "parallel": parallel,
        "data": data,
    }

    requestor = APIRequestor(**kwargs)
    return requestor.request("post", "meta.class.start", params=params)


def meta_exclusion_set_start(
    outcome: str = None,
    timeout: int = None,
    min_size_frac: float = None,
    # case_points: dict = None, DISABLED FOR NOW
    min_size: int = None,
    classes: List[str] = None,
    direction: Direction = Direction.both,
    encode: List[str] = None,
    depth: int = None,
    parallel: bool = False,
    data: List[Dict[str, Union[None, str, int, float]]] = None,
    **kwargs
):
    """
    Start a MetaMondo exploration using an exclusion set strategy.

    Feature rules are gathered by learning a rule, then learning again on the exclusion
    set (the set of data points outside of the rule), repeating until the exclusion set
    reaches a minimum number of data points.

    Parameters
    ----------
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

    outcome: str
        See **api.solve_start**

    data: List[dict]
        See **api.solve_start**

    timeout: int (optional)
        See **api.solve_start**

    min_size_frac: float (optional)
        See **api.solve_start**
    """
    params = {
        "outcome": outcome,
        "timeout": timeout,
        "min_size_frac": min_size_frac,
        "min_size": min_size,
        "classes": classes,
        "direction": direction,
        "encode": encode,
        "depth": depth,
        "parallel": parallel,
        "data": data,
    }

    requestor = APIRequestor(**kwargs)
    return requestor.request("post", "meta.exclusionset.start", params=params)


def meta_result(id: str, **kwargs):
    """Read meta solve results (rules) from the API

    Parameters
    ----------
    id: str
        The task ID as returned from **api.meta_class_start** or
        **api.meta_exclusion_set_start**
    """
    params = {"id": id}

    requestor = APIRequestor(**kwargs)

    return requestor.request("post", "meta.result", params=params)
