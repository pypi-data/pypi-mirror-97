from typing import Dict, List, Union

import numpy as np
import pandas as pd

from mondobrain.utils.graph import create_rule_graph


def _condition_mask(s: pd.Series, cond: Union[dict, str]):
    if isinstance(cond, dict):
        lo, hi = cond["lo"], cond["hi"]
        return (s >= lo) & (s <= hi)

    return s == cond


def conditions_mask(df: pd.DataFrame, rule: dict):
    """ Get a mask based on a dictionary of conditions
    """
    masks = []
    for key, cond in rule.items():
        masks.append(_condition_mask(df[key], cond))

    return np.all(np.array(masks), axis=0)


def apply_rule(df: pd.DataFrame, rule: dict, inverse: bool = False) -> pd.DataFrame:
    """ Applies the rule to the population df to obtain a sample

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to apply the rule to

    rule : dict
        A set of conditions to apply to the dataframe

    inverse : boolean, default=False
        If True, the inverse of the rule is applied

    Returns
    -------
    sample: pd.DataFrame
        The sample of the original dataframe based on rule conditions
    """
    if not rule:
        raise ValueError("An empty rule cannot be applied to a dataframe")

    mask = conditions_mask(df, rule)

    if inverse:
        mask = ~mask

    return df[mask]


def apply_rules(
    df: pd.DataFrame, rules: List[Dict], inverse: bool = False, operation: str = "or"
) -> pd.DataFrame:
    """ Applies a set of rules to the population df to obtain a sample

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to apply the rule to

    rule : List collection of Dict
        A list of a set of conditions to apply to the dataframe

    inverse : boolean, default=False
        If True, the inverse of the rule is applied

    operation : str, default="or"
        Options are "or" or "and"
        If "or", the union of the rules is applied
        If "and", the intersection of the rules is applied

    Returns
    -------
    sample: pd.DataFrame
        The sample of the original dataframe based on rule conditions
    """
    mask = [conditions_mask(df, rule) for rule in rules if rule]

    if len(mask) == 0:
        raise ValueError("No rule found to apply to the dataframe")

    if operation == "or":
        mask = np.any(mask, axis=0)
    elif operation == "and":
        mask = np.all(mask, axis=0)
    else:
        raise ValueError("operation type not supported")

    if inverse:
        mask = ~mask

    return df[mask]


def apply_rule_tree(
    df: pd.DataFrame, rule_tree: Dict, inverse: bool = False
) -> pd.DataFrame:
    """ Applies a set of hierarchical rules to the population df to obtain a sample

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to apply the rule to

    rule_tree : List collection of Dict
        A hierarchical set of conditions to apply to the dataframe

    inverse : boolean, default=False
        If True, the inverse of the rule is applied

    Returns
    -------
    sample: pd.DataFrame
        The sample of the original dataframe based on rule conditions
    """
    G = create_rule_graph(rule_tree)

    df_dict = dict()

    def segment_dataset(starting_node, df):
        rule = G.nodes[starting_node]["rule"]
        try:
            df_in = apply_rule(df, rule)
        except KeyError:
            df_in = df
        try:
            df_out = apply_rule(df, rule, inverse=True)
        except KeyError:
            df_out = df.loc[[]]
        neighbors = [
            node for node in G.neighbors(starting_node) if node != starting_node
        ]
        if neighbors:
            for node in neighbors:
                if node[-1] == "IN":
                    segment_dataset(node, df_in)
                elif node[-1] == "OUT":
                    segment_dataset(node, df_out)
        else:
            previous_level = starting_node[-2]
            current_level = previous_level + 1
            df_dict[starting_node + (current_level, "IN")] = df_in
            df_dict[starting_node + (current_level, "OUT")] = df_out

    segment_dataset((0, "IN", 0, "IN"), df)

    point_index = pd.concat(
        [df_dict[node] for node in df_dict if node[-1] == "IN"]
    ).index

    mask = np.in1d(df.index, point_index)
    if inverse:
        mask = ~mask

    return df[mask]
