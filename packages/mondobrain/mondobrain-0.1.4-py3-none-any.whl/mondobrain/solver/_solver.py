import io
from typing import List

import numpy as np
import pandas as pd

from mondobrain.api import solve_result, solve_start_file
import mondobrain.datautils as datautils
from mondobrain.dd_transformer import DDTransformer
from mondobrain.error import (
    DataTransformationError,
    InvalidTargetError,
    NotEnoughPointsError,
)
from mondobrain.metrics import score
from mondobrain.utils import constants, utilities
from mondobrain.utils.data import is_discrete


def solve(
    df: pd.DataFrame,
    outcome: str = None,
    target: str = None,
    encode=True,
    sample=True,
    random_state=None,
    return_diagnostics=False,
    **kwargs,
):
    """Run a solve without worrying about API requests.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to use for the solve

    outcome : str, default=None
        Which column to use as the outcome for the solve (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to target. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.

    encode: bool, default=True
        Whether or not the data should be encoded before being sent to the MB API.
        Encoding can result in additional time on client side. Disable if your data is
        largely non-sensitive.

    sample: bool, default=True
        Whether or not the data should be sampled before being sent to the MB API.
        Not pre-sampling the data can cause size limits to be reached and excessive
        solve times

    random_state : int or np.random.RandomStateInstance, default: 0
        Pseudo-random number generator to control the sampling state.
        Use an int for reproducible results across function calls.
        See the sklearn for more details.

    kwargs: any
        Remaining kwargs are sent so solve_start_file

    Returns
    -------
    rule: dict
        The conditions that the MB API found
    """
    if outcome is None:
        outcome = df.columns[0]

    if target is None:
        if df[outcome].dtype == np.object:
            target = df[outcome].iloc[0]
        else:
            target = "max"

    if target is np.nan:
        raise InvalidTargetError("Target cannot be NaN value")

    if encode:
        # Some utilities require original values
        df_orig = df.copy()
        outcome_orig = outcome
        target_orig = target

        encoder = DDTransformer(df)
        df = utilities.encode_dataframe(df, encoder)
        outcome = encoder.original_to_encoded_column(outcome)
        target = utilities.encode_value(df_orig, outcome_orig, target_orig, encoder)

    if sample:
        df = datautils.sample(
            df,
            2500,
            outcome=outcome,
            target=target,
            floor=3500,
            random_state=random_state,
        )

    _dimensionality_check(df, outcome, target)

    data = io.BytesIO()
    df.to_parquet(data)
    data.seek(0)  # Reset the pointer as `to_parquet` leaves it at the end

    task = solve_start_file(outcome=outcome, target=target, data=data, **kwargs)
    result = solve_result(id=task["id"])

    rule = result["rule"]
    diagnostics = result["diagnostics"]

    if encode:
        # We need to decode the rule & diagnostics if we encoded
        rule = utilities.decode_rule(rule, encoder)
        diagnostics = _decode_diagnostics(diagnostics, encoder)

    if return_diagnostics:
        return rule, diagnostics

    return rule


def _decode_diagnostics(diagnostics: dict, encoder: DDTransformer) -> dict:
    diagnostics = diagnostics.copy()

    try:
        disc_rules = diagnostics["discarded_rules"]["rules"]
        disc_rules = [utilities.decode_rule(r, encoder) for r in disc_rules]
        diagnostics["discarded_rules"]["rules"] = disc_rules
    except KeyError:
        pass

    return diagnostics


def _dimensionality_check(df: pd.DataFrame, outcome: str, target: str):
    col = df[outcome]

    if is_discrete(col):
        size = col[col == target].shape[0]
    else:
        if col.std() == 0:
            raise NotEnoughPointsError("Outcome column has no variance")

        size = col.shape[0]

    if size <= constants.MIN_SOLVER_SIZE:
        raise NotEnoughPointsError("Not enough points")


def _exhaustive_single(df: pd.DataFrame, outcome: str, target: str, **kwargs) -> List:
    try:
        rule = solve(df, outcome=outcome, target=target, **kwargs)
    except (NotEnoughPointsError, DataTransformationError):
        return []

    try:
        df_inverse = datautils.apply_rule(df, rule, inverse=True)
    except ValueError:
        df_inverse = df.loc[[]]

    if df_inverse.size > 0:
        return [rule] + _exhaustive_single(df_inverse, outcome, target, **kwargs)
    else:
        return []


def _exhaustive_best(df: pd.DataFrame, outcome: str, **kwargs) -> List:
    best_score = -99999.0
    for target in df[outcome].unique():
        try:
            rule = solve(df, outcome=outcome, target=target, **kwargs)
            if rule:
                rule_score = score(df, outcome, target, rule)
            else:
                rule_score = best_score
            if rule_score > best_score:
                best_rule = rule
                best_target = target
            else:
                continue
        except (NotEnoughPointsError, DataTransformationError):
            return []

        try:
            df_inverse = datautils.apply_rule(df, best_rule, inverse=True)
        except ValueError:
            df_inverse = df.loc[[]]

        if df_inverse.size > 0:
            return [[best_rule, best_target]] + _exhaustive_best(
                df_inverse, outcome, **kwargs
            )
        else:
            return []


def _exhaustive_any(df: pd.DataFrame, outcome: str, **kwargs) -> List:
    rule_set = []
    targets = df[outcome].unique()
    for target in targets:
        try:
            rule = solve(df, outcome=outcome, target=target, **kwargs)
            rule_set.append(rule)
        except (NotEnoughPointsError, DataTransformationError):
            return []

    try:
        df_inverse = datautils.apply_rules(df, rule_set, inverse=True)
    except ValueError:
        df_inverse = df.loc[[]]

    if df_inverse.size > 0:
        return [rule_set] + _exhaustive_any(df_inverse, outcome, **kwargs)
    else:
        return []


def exhaustive_solve(
    df: pd.DataFrame,
    outcome: str = None,
    target: str = None,
    approach: str = "single",
    **solve_params,
):
    """
        Build a set of conditions that exhaustively cover the entirety of a dataset

        Parameters
        ----------
        df: Pandas DataFrame
            Data values for the exhaustive solve containing Outcome Feature
            and Independent Feature variables.

        outcome : str
            The label of the dependent variable used for learning.

        target : str (optional), default=None
            The target class of the outcome. Applicable when running a
            exhaustive solve using the 'single' approach.

        approach : str (optional), default='single'
            The approach to use for exhaustive solves. Approaches have a different
            return shape.

            - ‘single’ (default) : (n_solves,)
                Search for rules on an individual target in a dataset.
            - ‘best’ : (2, n_solves)
                Generates rules for all targets, chooses the best rule and removes
                points in that rule. Repeats for remaining data.
            - ‘any’ : (n_classes, n_solves)
                Generates rules for all targets and removes points in any rule. Repeats
                for remaining data.

        **solve_params : any
            Parameters to pass on to `solve`

        Returns
        -------
        rule_set: List
            The set of conditions that the MB API found covering all points
            in the provided dataset
    """
    if outcome is None:
        outcome = df.columns[0]

    if approach == "single":
        return _exhaustive_single(df, outcome, target, **solve_params)
    if approach == "best":
        return _exhaustive_best(df, outcome, **solve_params)
    if approach == "any":
        return _exhaustive_any(df, outcome, **solve_params)

    raise ValueError(f"approach {approach} does not exist")
