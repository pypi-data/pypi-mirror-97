# flake8: noqa
import logging

__author__ = "MondoBrain"
__version__ = "0.1.4"

# Configuration variables
api_key = None
api_secret = None
api_token = None

api_base = "https://api.prod.mondobrain.com/"
auth0_domain = "mb-production.us.auth0.com"

verify_ssl_certs = True
proxy = None
default_http_client = None
enable_telemetry = True
max_network_retries = 0
ca_bundle_path = None

# Set to either 'debug' or 'info', controls console logging
log = None

from mondobrain import api  # isort:skip
from mondobrain.core.api import MondoDataFrame, MondoSeries  # isort:skip
from mondobrain.prescriber import Solver  # isort:skip
