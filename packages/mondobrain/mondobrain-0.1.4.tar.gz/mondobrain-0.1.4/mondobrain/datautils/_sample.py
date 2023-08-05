import numpy as np
import pandas as pd

from mondobrain.utils.data import is_discrete


def _uniform_stratified_sample(
    df: pd.DataFrame, size: int, outcome: str, random_state=None
) -> pd.DataFrame:
    return (
        df.groupby(outcome, group_keys=False)
        .apply(
            lambda x: x.sample(
                int(np.rint(size * x.shape[0] / df.shape[0])), random_state=random_state
            )
        )
        .sample(frac=1, random_state=random_state)
    )


def _oversampled_sample(
    df: pd.DataFrame, size: int, outcome: str, target: str, random_state=None
) -> pd.DataFrame:
    target_prob = 1 - (df[outcome] == target).sum() / df.shape[0]
    alternate_prob = 1 - target_prob

    pick = np.where(df[outcome] == target, target_prob, alternate_prob)

    weights = pick / pick.sum()

    return df.sample(size, random_state=random_state, weights=weights)


def sample(
    df: pd.DataFrame,
    size: int,
    outcome=None,
    target=None,
    floor: int = None,
    random_state=None,
):
    """Sample a dataframe while taking the outcome & target into consideration

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to sample

    outcome : str, default=None
        Which column to use as the outcome consideration (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to consider. For a continuous outcome this has
        no effect. If None, all targets are considered.

    floor: int, default=None
        The lower limit at which we should consider sampling. This lower limit is
        inclusive. If the number of rows is lte (<=) the floor, we return a copy of the
        dataframe

    random_state : int or np.random.RandomStateInstance, default: 0
        Pseudo-random number generator to control the sampling state.
        Use an int for reproducible results across function calls.
        See the sklearn for more details.


    Returns
    -------
    rule: dict
        The conditions that the MB API found
    """
    if floor is not None and df.shape[0] <= floor:
        return df.copy()

    if outcome is None:
        outcome = df.columns[0]

    # For discrete outcomes, we might use oversampled outcomes and the total number of
    # points are less than 0.15 of the overall
    if is_discrete(df[outcome]):

        # use uniform stratified sampling when target is not specified
        if target is None:
            return _uniform_stratified_sample(
                df, size, outcome, random_state=random_state
            )

        # if target is less than 15%, oversample the target
        if df[outcome].value_counts()[target] / df.shape[0] < 0.15:
            return _oversampled_sample(
                df, size, outcome, target, random_state=random_state
            )

        # if outcome only has 2 classes, check alternate for oversample conditions
        if df[outcome].value_counts().shape[0] == 2:
            modalities = df[outcome].value_counts().index
            alternate = modalities[~np.in1d(modalities, target)][0]

            # if the alternate target is less than 15%, oversample it
            if df[outcome].value_counts()[alternate] / df.shape[0] < 0.15:
                return _oversampled_sample(
                    df, size, outcome, alternate, random_state=random_state
                )

    # Continuous outcomes get sampled regularly, as well as any discrete that don't
    # meet the above conditions
    return df.sample(size, random_state=random_state)
