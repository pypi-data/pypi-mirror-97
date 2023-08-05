import pandas as pd


def _decorrelate_matrix(
    df: pd.DataFrame,
    method: str = "spearman",
    encode: bool = True,
    outcome: str = None,
    threshold: float = 0.5,
) -> pd.DataFrame:

    from mondobrain.metrics import correlation_groups, correlation_matrix

    corr_matrix = correlation_matrix(df, method=method, encode=encode)
    groups = correlation_groups(corr_matrix, outcome=outcome, threshold=threshold)

    cols = []
    if outcome:
        cols.append(outcome)
    cols += [x["name"] for x in groups]

    return df[cols] if len(cols) > 0 else df


def _decorrelate_signals(
    df: pd.DataFrame,
    threshold: [float, float] = None,
    outcome: str = None,
    target: str = None,
    **solve_params
) -> pd.DataFrame:

    from mondobrain.metrics import feature_signals

    if threshold is not None and (
        len(threshold) != 2
        or (
            threshold[0] is not None
            and threshold[1] is not None
            and threshold[0] >= threshold[1]
        )
    ):
        raise ValueError(
            "Threshold must be [min, max] where min < max, [None, max] or [min, None]."
        )

    signals = feature_signals(df, outcome=outcome, target=target, **solve_params)

    cols = []
    if outcome:
        cols.append(outcome)

    for col, data in signals.items():
        if threshold is not None:
            if threshold[0] is not None and data["score"] < threshold[0]:
                continue
            if threshold[1] is not None and data["score"] > threshold[1]:
                continue

        cols.append(col)

    return df[cols] if len(cols) > 0 else df


def decorrelate(df: pd.DataFrame, technique: str = "signals", **kwargs) -> pd.DataFrame:
    """
    Remove highly correlated columns in a dataframe.

    Parameters
    ----------
    df: Pandas DataFrame
        Dataframe containing variables that you want to decorrelate.

    technique: str {'signals', 'matrix'}, default='signals'
        Decorrelation technique used.
        If 'signals', it uses the mondobrain.metrics.feature_signals function to remove
        feature variables that have a score below a specified threshold.
        If 'matrix', it uses the mondobrain.metrics.correlation_matrix function to
        selection correlation group heads based on a specified threshold.

    **kwargs
        Arguments to pass to the corresponding functions in the mondobrain.metrics
        package.

    Returns
    -------
    decorrelated_df: Pandas Dataframe
        A dataframe with the columns correlated above the specified threshold
        removed.
    """
    if technique == "signals":
        return _decorrelate_signals(df, **kwargs)
    elif technique == "matrix":
        return _decorrelate_matrix(df, **kwargs)
    else:
        raise ValueError("Invalid technique '%s' given." % technique)
