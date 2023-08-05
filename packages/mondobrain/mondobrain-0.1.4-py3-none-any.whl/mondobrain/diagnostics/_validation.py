import numpy as np
import pandas as pd
from sklearn.model_selection import KFold, train_test_split

from mondobrain.datautils import apply_rule
from mondobrain.metrics import score
from mondobrain.solver import solve


def cross_validate(df: pd.DataFrame, cv=3, random_state=1337, **kwargs):
    if isinstance(cv, (int, float)):
        cv = KFold(n_splits=cv, shuffle=True)

    train, test = train_test_split(df, test_size=0.33, random_state=random_state)

    rules = []
    train_sizes, train_scores = [], []
    test_sizes, test_scores = [], []

    for train_idx, _ in cv.split(train):
        train_curr = train.iloc[train_idx]

        rule = solve(train_curr, random_state=random_state, **kwargs)
        if not rule:
            continue

        rules.append(rule)

        # Get train metrics
        train_applied = apply_rule(train_curr, rule)

        train_size, _ = train_applied.shape
        train_score = score(train_applied, population=train_curr, **kwargs)

        train_sizes.append(train_size)
        train_scores.append(train_score)

        # Get test metrics
        test_applied = apply_rule(test, rule)

        test_size, _ = test_applied.shape
        test_score = score(test_applied, population=test, **kwargs)

        test_sizes.append(test_size)
        test_scores.append(test_score)

    mse = np.mean((np.array(train_scores) - np.array(test_scores)) ** 2)

    return {
        "avg_loss": mse,
        "train_scores": train_scores,
        "train_sizes": train_sizes,
        "test_scores": test_scores,
        "test_sizes": test_sizes,
        "rules": rules,
    }
