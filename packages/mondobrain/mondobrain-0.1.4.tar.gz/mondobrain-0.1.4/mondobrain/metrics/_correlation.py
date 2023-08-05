from typing import List, Mapping

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

from mondobrain.utils.data import is_discrete

Matrix = Mapping[str, Mapping[str, float]]


def correlation_matrix(
    df: pd.DataFrame, method: str = "spearman", encode: bool = True
) -> Matrix:
    """
    Compute the correlation matrix of each column in the dataframe.

    Parameters
    ----------
    df: Pandas DataFrame
        Dataframe containing variables that you want to calculate the correlation of.

    method: str {'spearman', 'tau', 'pearson'}, default='spearman'
        Correlation algorithm to use

    encode: bool, default=True
        If True, categorical variables are one hot encoded and the maximum correlation
        of a category is taken.  If False, no encoding takes place.

    Returns
    -------
    corr_matrix: dict
        A nested dictionary that maps variable -> other variable -> correlation value
        between -1 and 1, inclusive.

    Examples
    --------
    >>> from mondobrain.datasets import load_iris
    >>> df = load_iris()
    >>> correlation_matrix(df)
    array([[2, 0, 0],
           [0, 0, 1],
           [1, 0, 2]])
    >>> y_true = ["cat", "ant", "cat", "cat", "ant", "bird"]
    >>> y_pred = ["ant", "ant", "cat", "cat", "ant", "cat"]
    >>> confusion_matrix(y_true, y_pred, labels=["ant", "bird", "cat"])
    {
        "SepalLength": {
            "PetalLength": 0.8813863932886515,
            "PetalWidth": 0.8344206519767946,
            "SepalWidth": -0.15945651848582867
        },
        "SepalWidth": {
            "PetalLength": -0.3034206463815158,
            "PetalWidth": -0.2775110724763029,
            "SepalLength": -0.15945651848582867
        },
        "PetalLength": {
            "PetalWidth": 0.9360033509355781,
            "SepalLength": 0.8813863932886515,
            "SepalWidth": -0.3034206463815158
        },
        "PetalWidth": {
            "PetalLength": 0.9360033509355781,
            "SepalLength": 0.8344206519767946,
            "SepalWidth": -0.2775110724763029
        }
    }

    """

    def one_hot_enc_label(value):
        for ohe_col in one_hot_enc_cols:
            if value.startswith(ohe_col):
                return ohe_col
        return value

    def abs_max(series):
        if series.size == 0:
            return 0

        col = series.sort_values()
        a, b = col[0], col[col.size - 1]

        return a if np.abs(a) >= np.abs(b) else b

    df_copy = df.copy()

    # convert to str to ensure that sortable types. Sometimes dates mess this up
    for col in df_copy.columns:
        if is_discrete(df[col]):
            df_copy[col] = df_copy[col].astype(str)

    # using DDTransformer as encoder drops columns, so use LabelEncoder instead
    edf = df_copy.apply(LabelEncoder().fit_transform)
    one_hot_enc_cols = [
        col
        for col in edf.columns
        if is_discrete(edf[col]) and len(edf[col].unique()) <= 12
    ]

    if encode:
        edf = pd.get_dummies(edf, columns=one_hot_enc_cols)

    df_corr = edf.corr(method=method)
    df_corr = df_corr.fillna(0)

    if encode:
        df_corr = df_corr.groupby(one_hot_enc_label, axis=0).agg(abs_max)
        df_corr = df_corr.groupby(one_hot_enc_label, axis=1).agg(
            lambda x: x.agg(abs_max, axis=1)
        )

    corr_matrix = df_corr.to_dict()
    corr_matrix = {
        out_var: {
            in_var: corr
            for in_var, corr in sorted(map.items(), key=lambda x: -np.abs(x[1]))
            if out_var != in_var
        }
        for out_var, map in corr_matrix.items()
    }

    return corr_matrix


def correlation_groups(
    corr_matrix: Matrix, outcome: str = None, threshold: float = 0.5
) -> List[dict]:
    """
    Build groups of correlated variables based on their correlation matrix.

    Parameters
    ----------
    corr_matrix: Matrix
        A correlation matrix built by the `correlation_matrix` function.

    outcome: str, default=None
        If given, variables are sorted by their correlation to the outcome before
        grouping.  This ensures that variables with the highest importance with respect
        to the outcome are group heads.

    threshold: float, default=0.5
        Minimum threshold to assign a variable to a group.  If the correlation between
        a variable and a group head is at least the threshold value, then the variable
        is placed in that group.

    Returns
    -------
    groups: List[dict]
        A list of groups, each with a head variable and a sub-list of variables in
        that group.

    Examples
    --------
    >>> from mondobrain.datasets import load_iris
    >>> df = load_iris()
    >>> correlation_groups(df)
    [
        {
            "name": "PetalWidth",
            "variables": [
            {
                "name": "PetalLength",
                "correlationToHead": 0.9360033509355781,
                "correlationToOutcome": -0.8173907505619173
            },
            {
                "name": "SepalLength",
                "correlationToHead": 0.8344206519767946,
                "correlationToOutcome": -0.7495899411738537
            }
            ],
            "correlationToOutcome": -0.8202403166214466
        },
        {
            "name": "SepalWidth",
            "variables": [],
            "correlationToOutcome": 0.6163483317643264
        }
    ]

    """
    if threshold < 0 or threshold > 1:
        raise ValueError("Threshold must be a float between 0 and 1, inclusive.")

    groups = []

    if outcome:
        vars = sorted(
            (k for k in corr_matrix.keys() if k != outcome),
            key=lambda x: -np.abs(corr_matrix[x][outcome]),
        )
    else:
        vars = corr_matrix.keys()
    used_vars = {x: False for x in vars}

    for head in vars:
        if used_vars[head]:
            continue

        sub_groups = []

        for sub, corr in corr_matrix[head].items():
            if (outcome and sub == outcome) or used_vars[sub]:
                continue
            if np.abs(corr) < threshold:
                break

            used_vars[sub] = True
            sub_data = {
                "name": sub,
                "correlationToHead": corr,
            }
            if outcome:
                sub_data.update({"correlationToOutcome": corr_matrix[sub][outcome]})
            sub_groups.append(sub_data)

        head_data = {"name": head, "variables": sub_groups}
        if outcome:
            head_data.update({"correlationToOutcome": corr_matrix[head][outcome]})

        groups.append(head_data)

    return groups
