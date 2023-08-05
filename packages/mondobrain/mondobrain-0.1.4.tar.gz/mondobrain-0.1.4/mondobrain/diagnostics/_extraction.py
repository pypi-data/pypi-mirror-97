import numpy as np
import pandas as pd

from mondobrain.solver import solve
from mondobrain.utils.data import is_continuous


def extract_rule(
    df: pd.DataFrame,
    predicted: np.ndarray,
    outcome: str = None,
    target: str = None,
    random_state=None,
    **kwargs,
):
    # Make local copy of the df
    df = df.copy()

    if outcome is None:
        outcome = df.columns[0]

    if target is None:
        target = "max" if is_continuous(df[outcome]) else "correct"

    if is_continuous(df[outcome]):
        if target not in ["max", "min"]:
            raise ValueError("target must be `min` or `max` when outcome is continuous")

        df["__error"] = np.abs(predicted - df[outcome])
    else:
        if target not in ["correct", "incorrect"]:
            raise ValueError(
                "target must be `correct` or `incorrect` when outcome is discrete"
            )

        df["__error"] = np.where((predicted == df[outcome]), "correct", "incorrect")

    solve_df = df.drop(outcome, axis=1)
    return solve(
        solve_df, outcome="__error", target=target, random_state=random_state, **kwargs
    )
