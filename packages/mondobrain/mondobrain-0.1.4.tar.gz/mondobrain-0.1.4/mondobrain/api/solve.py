from io import BytesIO
from typing import Dict, List, Union

from mondobrain.api.requestor import APIRequestor


def solve_start(
    outcome: str = None,
    target: str = None,
    data: List[Dict[str, Union[None, str, int, float]]] = None,
    timeout: int = None,
    min_size_frac: float = None,
    case_points: dict = None,
    **kwargs
):
    """Used for starting a solve using inline data (array of dicts)

    Parameters
    ----------
    outcome: str
        The feature to use as your outcome

    target: str
        The target for the outcome feature

    data: List[dict]
        The rows of data to use

    timeout: int (optional)
        The timeout to apply to the Solver loop. Defaults to API value

    min_size_frac: float (optional)
        Value between 0.0 and 1.0 that defines the minimum number of points needed for
        a valid rule discovered by the API

    case_points: dict
        Dictionary definining case points to include in rule
    """
    params = {
        "outcome": outcome,
        "target": target,
        "data": data,
        "timeout": timeout,
        "min_size_frac": min_size_frac,
        "case_points": case_points,
    }

    requestor = APIRequestor(**kwargs)

    return requestor.request("post", "solve.start", params=params)


def solve_start_file(
    outcome: str = None,
    target: str = None,
    data: BytesIO = None,
    timeout: int = None,
    min_size_frac: float = None,
    case_points: dict = None,
    **kwargs
) -> dict:
    """Used for starting a solve using a file to "carry" the data

    Parameters
    ----------
    outcome: str
        The feature to use as your outcome

    target: str
        The target for the outcome feature

    data: io.BytesIO
        A parquet buffer of the dataset
    """
    params = {
        "outcome": outcome,
        "target": target,
        "data": data,
        "timeout": timeout,
        "min_size_frac": min_size_frac,
        "case_points": case_points,
    }

    requestor = APIRequestor(**kwargs)
    supplied_headers = {"Content-Type": "multipart/form-data"}
    return requestor.request(
        "post", "solve.start.file", params=params, headers=supplied_headers
    )


def solve_result(id: str, **kwargs):
    """Read solve results (rules) from the API

    Parameters
    ----------
    id: str
        The task ID as returned from **api.solve_start** or **api.solve_start_file**
    """
    params = {"id": id}

    requestor = APIRequestor(**kwargs)

    return requestor.request("post", "solve.result", params=params)
