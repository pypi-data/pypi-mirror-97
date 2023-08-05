import logging
import os
import re
import sys

import mondobrain

MONDOBRAIN_LOG = os.environ.get("MONDOBRAIN_LOG")

logger = logging.getLogger("mondobrain")


def _console_log_level():
    if mondobrain.log in ["debug", "info"]:
        return mondobrain.log
    elif MONDOBRAIN_LOG in ["debug", "info"]:
        return MONDOBRAIN_LOG
    else:
        return None


def log_debug(message, **params):
    msg = logfmt(message, dict(**params))
    if _console_log_level() == "debug":
        print(msg, file=sys.stderr)
    logger.debug(msg)


def log_info(message, **params):
    msg = logfmt(message, dict(**params))
    if _console_log_level() in ["debug", "info"]:
        print(msg, file=sys.stderr)
    logger.info(msg)


def logfmt(message, props: dict):
    def fmt(key: str, val):
        if hasattr(val, "decode"):
            val = val.decode("utf-8")

        if not isinstance(val, str):
            val = str(val)

        if re.search(r"\s", val):
            val = repr(val)

        if re.search(r"\s", key):
            key = repr(key)

        return "{key}={val}".format(key=key, val=val)

    prop_str = " ".join([fmt(key, val) for key, val in sorted(props.items())])

    return "%s %s" % (message, prop_str)
