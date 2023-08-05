class MondobrainError(Exception):
    pass


class APIError(MondobrainError):
    def __init__(
        self,
        message=None,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
    ):
        super(APIError, self).__init__(message)

        if http_body and hasattr(http_body, "decode"):
            try:
                http_body = http_body.decode("utf-8")
            except BaseException:
                http_body = "<Could not decode body as utf-8>"

        self._message = message
        self.http_body = http_body
        self.json_body = json_body
        self.headers = headers or {}
        self.code = code
        self.request_id = self.headers.get("x-request-id", None)

    def __str__(self):
        msg = self._message or "<empty message>"
        if self.request_id is not None:
            return u"Request {0}: {1}".format(self.request_id, msg)

        return msg

    def __repr__(self):
        return "%s(message=%r, http_status=%r, request_id=%r)" % (
            self.__class__.__name__,
            self._message,
            self.http_status,
            self.request_id,
        )


class APIConnectionError(APIError):
    def __init__(
        self,
        message,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        should_retry=False,
    ):
        super(APIConnectionError, self).__init__(
            message, http_body, http_status, json_body, headers, code
        )
        self.should_retry = should_retry


class AuthenticationError(APIError):
    pass


class PermissionError(APIError):
    pass


class ProcessingError(APIError):
    def __init__(
        self,
        message,
        http_body=None,
        http_status=None,
        json_body=None,
        headers=None,
        code=None,
        type=None,
    ):
        super(ProcessingError, self).__init__(
            message, http_body, http_status, json_body, headers, code
        )

        self.type = type


class InvalidTargetError(MondobrainError):
    pass


class NotEnoughPointsError(MondobrainError):
    pass


class DataTransformationError(MondobrainError):
    pass
