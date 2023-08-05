import json
import platform

import mondobrain
from mondobrain import error, utils
from mondobrain.api import clients
from mondobrain.api.util import encode_multipart, get_token


class APIRequestor(object):
    def __init__(self, token=None, client=None, api_base=None):
        self.api_base = api_base or mondobrain.api_base
        self.api_token = token or mondobrain.api_token

        if token:
            self.api_token = token
        elif mondobrain.api_token:
            self.api_token = mondobrain.api_token
        else:
            mondobrain.api_token = get_token(mondobrain.api_key, mondobrain.api_secret)
            self.api_token = mondobrain.api_token

        if client:
            self._client = client
        elif mondobrain.default_http_client:
            self._client = mondobrain.default_http_client
        else:
            mondobrain.default_http_client = clients.new_default_http_client()
            self._client = mondobrain.default_http_client

    def request(self, method, url, params=None, headers=None):
        rbody, rcode, rheaders = self.request_raw(method.lower(), url, params, headers)

        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp

    def handle_error_response(self, rbody, rcode, resp, rheaders):
        try:
            error_data = {"type": resp["type"], "message": resp["message"]}

            code = resp.get("code", None)
            if code is not None:
                error_data["code"] = code
        except (KeyError, TypeError):
            raise error.APIError(
                "Invalid response object from API: %r "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody,
                rcode,
                resp,
                rheaders,
            )

        msg = error_data.get("message", None)

        if rcode == 401:
            raise error.AuthenticationError(msg, rbody, rcode, resp, rheaders, code)

        elif rcode == 402:
            eType = error_data["type"]
            raise error.ProcessingError(msg, rbody, rcode, resp, rheaders, code, eType)

        elif rcode == 403:
            raise error.PermissionError(msg, rbody, rcode, resp, rheaders, code)

        else:
            raise error.APIError(msg, rbody, resp, rheaders)

    def request_headers(self, api_token):
        user_agent = "Mondobrain/v1 PythonBindings/%s" % (mondobrain.__version__,)

        ua = {
            "bindings_version": mondobrain.__version__,
            "lang": "python",
            "publisher": "mondobrain",
            "httplib": "requests",
            "lang_version": platform.python_version(),
            "platform": platform.platform(),
            "uname": " ".join(platform.uname()),
        }

        headers = {
            "X-Mondobrain-Client-User-Agent": json.dumps(ua),
            "User-Agent": user_agent,
            "Authorization": "Bearer %s" % (api_token,),
            "Content-Type": "application/json",
        }

        return headers

    def request_raw(self, method, url, params=None, supplied_headers=None):
        """
        Mechanism for issuing an API call
        """

        # TODO: token flow
        my_api_token = self.api_token

        abs_url = "%s%s" % (self.api_base, url)

        if (
            supplied_headers is not None
            and supplied_headers.get("Content-Type") == "multipart/form-data"
        ):
            post_data, content_type = encode_multipart(params)
            supplied_headers["Content-Type"] = content_type
        else:
            params = {k: v for k, v in params.items() if v is not None}
            post_data = json.dumps(params)

        headers = self.request_headers(my_api_token)
        if supplied_headers is not None:
            for key, value in supplied_headers.items():
                headers[key] = value

        utils.log_info("Request to Mondobrain api", method=method, path=abs_url)
        utils.log_debug("Post details", post_data=params)

        rbody, rcode, rheaders = self._client.request_with_polling(
            method, abs_url, headers, post_data
        )

        utils.log_info("Mondobrain API response", path=abs_url, response_code=rcode)
        utils.log_debug("API response body", body=rbody)

        return rbody, rcode, rheaders

    def interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, "decode"):
                rbody = rbody.decode("utf-8")

            data = json.loads(rbody)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody,
                rcode,
                headers=rheaders,
            )

        if not 200 <= rcode < 300:
            self.handle_error_response(rbody, rcode, data, rheaders)

        return data
