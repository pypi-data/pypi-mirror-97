import numpy as np
import pandas as pd

from mondobrain.datautils import apply_rule
from mondobrain.dd_transformer import DDTransformer
from mondobrain.utils import utilities
from mondobrain.utils.data import is_continuous

from ._target import target_metrics


def score(
    df: pd.DataFrame,
    outcome: str = None,
    target: str = None,
    rule: dict = None,
    population: pd.DataFrame = None,
):
    """Score a dataframe

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to score. If rule is set, then df should represent the original
        population. If population is set, then df should represent the sample to score.

    outcome : str, default=None
        Which column to use as the outcome for the score (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to target. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.

    rule: dict, default=None
        The solver rule to use for scoring. This or population must be set, but not
        both. If set, df should be the population dataset

    population: pd.DataFrame, default=None
        The population dataset to base the score off of. If set, df should be the sample
        dataset.

    Returns
    -------
    score: float
        The score of the sample and population
    """
    # Quick checks to make sure that one of rule and population is set.
    if rule is None and population is None:
        raise ValueError("one of `rule` or `population` must be set")

    if rule is not None and population is not None:
        raise ValueError("only one of `rule` or `population` may be set")

    if outcome is None:
        outcome = df.columns[0]

    if target is None:
        target = df[outcome].iloc[0] if df[outcome].dtype == np.object else "max"

    if population is not None:
        sample = df

    if rule is not None:
        population = df
        sample = apply_rule(df, rule)

    # Encode our outcome column if the outcome column is continuous
    if is_continuous(population[outcome].dtype):
        encoder = DDTransformer(population)
        population = utilities.encode_dataframe(population, encoder)
        sample = utilities.encode_dataframe(sample, encoder)

        # Encode outcome. Target not needed as this is continuous
        outcome = encoder.original_to_encoded_column(outcome)

    # Get metrics for population and sample
    pop_metrics = target_metrics(population[outcome], target)
    smp_metrics = target_metrics(sample[outcome], target)

    # Return 0 if we our size is 0
    if smp_metrics["size"] == 0 or pop_metrics["size"] == 0:
        return 0

    return (
        np.sqrt(smp_metrics["size"])
        * (smp_metrics["mean"] - pop_metrics["mean"])
        / pop_metrics["std"]
    )


def _exclude_key(a: dict, key) -> dict:
    return {k: v for k, v in a.items() if k != key}


def partial_scores(
    df: pd.DataFrame, rule: dict, outcome: str = None, target: str = None,
) -> dict:
    """Calculates the partial score for each condition in a rule.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to score. The df should represent the original
        population.

    rule: dict
        The solver rule to use for scoring.

    outcome : str, default=None
        Which column to use as the outcome for the score (sometimes referred to as a
        target feature). If None, then the first column is selected

    target: str, default=None
        The class in the outcome column to target. For a continuous outcome this should
        either be `min` or `max`. If None, then the first class or `max` is selected.


    Returns
    -------
    scores: dict
        A dictionary of scores for each key/condition in the rule
    """
    if not rule:
        raise ValueError("An empty rule is not permitted")

    base_score = score(df, outcome=outcome, target=target, rule=rule)

    if len(rule.keys()) == 1:
        key = list(rule.keys())[0]
        return {key: base_score}

    scores = {}
    for key, cond in rule.items():
        subrule = _exclude_key(rule, key)
        subscore = score(df, outcome=outcome, target=target, rule=subrule)

        scores[key] = base_score - subscore

    return scores


def feature_signals(
    df: pd.DataFrame, outcome: str = None, target: str = None, **solve_params,
):
    """
    Calculate the signal/strength of each variable in a dataframe.

    Parameters
    ----------
    df: Pandas DataFrame
        Dataframe containing the Outcome Feature and Independent Feature variables.

    outcome: str (optional), default=None
        The label of the dependent variable used for learning.  If None, the first
        column is used.

    target: str (optional), default=None
        The target class of the outcome if discrete.  'min' or 'max' if continuous.

    **solve_params: any
        Parameters to pass on to `solve`

    Returns
    -------
    signals: dict
        A dictionary mapping each variable with their score and condition
        leading to the score.  This is achieved by doing a one dimensional
        solve on each variable.
    """
    from ..solver import solve

    if not outcome:
        outcome = df.columns[0]

    results = {}

    for col in df.columns:
        if col == outcome:
            continue

        df_one_dim = df[[col, outcome]]

        rule = solve(df_one_dim, outcome=outcome, target=target, **solve_params)
        rule_score = score(df, outcome, target, rule) if rule else 0

        results[col] = {"condition": rule[col] if rule else {}, "score": rule_score}

    sorted_results = {
        k: v
        for k, v in sorted(results.items(), key=lambda x: x[1]["score"], reverse=True)
    }

    return sorted_results
