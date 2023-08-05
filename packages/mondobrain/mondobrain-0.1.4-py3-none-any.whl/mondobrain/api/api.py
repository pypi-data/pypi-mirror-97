from .requestor import APIRequestor


def api_test(error: str = None, **kwargs):
    """Tests the ability to connect to the API
    """
    params = {}
    if error:
        params["error"] = error

    requestor = APIRequestor(**kwargs)

    return requestor.request("post", "api.test", params=params)
