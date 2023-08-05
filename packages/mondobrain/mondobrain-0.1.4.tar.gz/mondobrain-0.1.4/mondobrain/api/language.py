from .requestor import APIRequestor


def language_entities(message: str, metadata: dict, **kwargs):
    """Use the API to extract entities in a sentence
    """
    params = {
        "message": message,
        "metadata": metadata,
    }

    requestor = APIRequestor(**kwargs)
    return requestor.request("post", "language.entities", params=params)
