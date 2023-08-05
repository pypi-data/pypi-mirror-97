from .requestor import APIRequestor


def auth_test(error: str = None, **kwargs):
    """Tests validity of your credentials
    """
    params = {}
    if error:
        params["error"] = error

    requestor = APIRequestor(**kwargs)

    return requestor.request("post", "auth.test", params=params)
