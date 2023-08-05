import json
import random
import textwrap
import threading
import time

import requests

import mondobrain
from mondobrain import error, utils


def _now_ms():
    return int(round(time.time() * 1000))


def new_default_http_client(*args, **kwargs):
    return RequestsClient(*args, **kwargs)


class HTTPClient(object):
    MAX_DELAY = 2
    INITIAL_DELAY = 0.5
    MAX_RETRY_AFTER = 60

    def __init__(self):
        self._thread_local = threading.local()

    def request_with_polling(self, method, url, headers, post_data=None):
        """Handles retrying requests that are known to require polling
        """
        num_polls = 0

        while True:
            try:
                response = self.request_with_retries(method, url, headers, post_data)
                connection_error = None
            except error.APIConnectionError as e:
                connection_error = e
                response = None

            if self._should_poll(response):
                num_polls += 1
                sleep_time = self._sleep_time_seconds(num_polls, response)
                utils.log_info(
                    (
                        "Initiating poll %i for request %s %s after "
                        "sleeping %.2f seconds." % (num_polls, method, url, sleep_time)
                    )
                )

                time.sleep(sleep_time)

            else:
                if response is not None:
                    return response
                else:
                    raise connection_error

    def request_with_retries(self, method, url, headers, post_data=None):
        """
            Handles network retries.
        """
        self._add_telemetry_header(headers)

        num_retries = 0

        while True:
            try:
                response = self.request(method, url, headers, post_data)
                connection_error = None
            except error.APIConnectionError as e:
                connection_error = e
                response = None

            if self._should_retry(response, connection_error, num_retries):
                if connection_error:
                    utils.log_info(
                        "Encountered a retryable error %s" % str(connection_error)
                    )

                num_retries += 1
                sleep_time = self._sleep_time_seconds(num_retries, response)
                utils.log_info(
                    (
                        "Initiating retry %i for request %s %s after "
                        "sleeping %.2f seconds."
                        % (num_retries, method, url, sleep_time)
                    )
                )

                time.sleep(sleep_time)
            else:
                if response is not None:
                    return response
                else:
                    raise connection_error

    def request(self, method, url, headers, post_data=None):
        raise NotImplementedError("HTTPClient subclasses must implement `request`")

    def _should_retry(self, response, api_connection_error, num_retries):
        if num_retries >= self._max_network_retries():
            return False

        if response is None:
            return api_connection_error.should_retry

        _, status_code, rheaders = response

        if rheaders is not None and "mondobrain-should-retry" in rheaders:
            if rheaders["mondobrain-should-retry"] == "false":
                return False
            if rheaders["mondobrain-should-retry"] == "true":
                return True

        if status_code >= 500:
            return True

        return False

    def _should_poll(self, response):
        if not response:
            return False

        _, status_code, _ = response

        if status_code == 202:
            return True

        return False

    def _max_network_retries(self):
        from mondobrain import max_network_retries

        return max_network_retries

    def _retry_after_header(self, response=None):
        if response is None:
            return None

        _, _, rheaders = response

        try:
            return int(rheaders["retry-after"])
        except (KeyError, ValueError):
            return None

    def _sleep_time_seconds(self, num_retries, response=None):
        sleep_seconds = min(
            HTTPClient.INITIAL_DELAY * (2 ** (num_retries - 1)), HTTPClient.MAX_DELAY
        )

        sleep_seconds = self._add_jitter_time(sleep_seconds)

        # But never sleep less than initial delay
        sleep_seconds = max(HTTPClient.INITIAL_DELAY, sleep_seconds)

        # And never sleep less than the time the API asks us to wait,
        # assuming it's a reasonable ask.
        retry_after = self._retry_after_header(response) or 0
        if retry_after <= HTTPClient.MAX_RETRY_AFTER:
            sleep_seconds = max(retry_after, sleep_seconds)

        return sleep_seconds

    def _add_jitter_time(self, sleep_seconds):
        # Randomize the value in [(sleep_seconds/ 2) to (sleep_seconds)]
        # Also separated method here to isolate randomness for tests
        sleep_seconds *= 0.5 * (1 + random.uniform(0, 1))
        return sleep_seconds

    def _add_telemetry_header(self, headers):
        last_request_metrics = getattr(self._thread_local, "last_request_metrics", None)
        if mondobrain.enable_telemetry and last_request_metrics:
            telemetry = {"last_request_metrics": last_request_metrics}
            headers["X-Mondobrain-Client-Telemetry"] = json.dumps(telemetry)

    def _record_request_metrics(self, response, request_start):
        _, _, rheaders = response
        if "X-Request-Id" in rheaders and mondobrain.enable_telemetry:
            request_id = rheaders["X-Request-Id"]
            request_duration_ms = _now_ms() - request_start
            self._thread_local.last_request_metrics = {
                "request_id": request_id,
                "request_duration_ms": request_duration_ms,
            }

    def close(self):
        raise NotImplementedError("HTTPClient subclasses must implement `close`")


class RequestsClient(HTTPClient):
    name = "requests"

    def __init__(self, timeout=80, session=None, **kwargs):
        super(RequestsClient, self).__init__(**kwargs)
        self._session = session
        self._timeout = timeout

    def request(self, method, url, headers, post_data=None):
        kwargs = {}
        if getattr(self._thread_local, "session", None) is None:
            self._thread_local.session = self._session or requests.Session()

        try:
            try:
                result = self._thread_local.session.request(
                    method,
                    url,
                    headers=headers,
                    data=post_data,
                    timeout=self._timeout,
                    **kwargs
                )
            except TypeError as e:
                raise TypeError(
                    "Warning: It looks like your installed version of the "
                    '"requests" library is not compatible with Mondobrain\'s '
                    "usage thereof. (HINT: The most likely cause is that "
                    'your "requests" library is out of date. You can fix '
                    'that by running "pip install -U requests".) The '
                    "underlying error was: %s" % (e,)
                )

            content = result.content
            status_code = result.status_code
        except Exception as e:
            self._handle_request_error(e)

        return content, status_code, result.headers

    def _handle_request_error(self, e):
        # Catch SSL error first as it belongs to ConnectionError,
        # but we don't want to retry
        if isinstance(e, requests.exceptions.SSLError):
            msg = (
                "Could not verify Mondobrain's SSL certificate. Please make "
                "sure that your network is not intercepting certificates. "
                "If this problem persists, reach out to your representative"
            )

            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = False

        # Retry only timeout and connect errors; similar to urllib3 Retry
        elif isinstance(
            e, (requests.exceptions.Timeout, requests.exceptions.ConnectionError),
        ):
            msg = (
                "Unexpected error communicating with Mondobrain. "
                "If this problem persists, reach out to your representative"
            )

            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = True

        # Catch remaining request exceptions
        elif isinstance(e, requests.exceptions.RequestException):
            msg = (
                "Unexpected error communicating with Mondobrain. "
                "If this problem persists, reach out to your representative"
            )

            err = "%s: %s" % (type(e).__name__, str(e))
            should_retry = False

        else:
            msg = (
                "Unexpected error communicating with Mondobrain. "
                "It looks like there's probably a configuration "
                "issue locally.  If this problem persists, reach out"
                "to your representative"
            )
            err = "A %s was raised" % (type(e).__name__,)
            if str(e):
                err += " with error message %s" % (str(e),)
            else:
                err += " with no error message"
            should_retry = False

        msg = textwrap.fill(msg) + "\n\n(Network error %s)" % (err,)
        raise error.APIConnectionError(msg, should_retry=should_retry)

    def close(self):
        if getattr(self._thread_local, "session", None) is not None:
            self._thread_local.session.close()
