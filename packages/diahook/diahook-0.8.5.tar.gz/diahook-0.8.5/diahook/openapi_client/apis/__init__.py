
# flake8: noqa

# Import all APIs into this package.
# If you have many APIs here with many many models used in each API this may
# raise a `RecursionError`.
# In order to avoid this, import only the API that you directly need like:
#
#   from .api.application_api import ApplicationApi
#
# or import this package, but before doing it, use:
#
#   import sys
#   sys.setrecursionlimit(n)

# Import APIs into API package:
from diahook.openapi_client.api.application_api import ApplicationApi
from diahook.openapi_client.api.authentication_api import AuthenticationApi
from diahook.openapi_client.api.development_api import DevelopmentApi
from diahook.openapi_client.api.endpoint_api import EndpointApi
from diahook.openapi_client.api.health_api import HealthApi
from diahook.openapi_client.api.message_api import MessageApi
from diahook.openapi_client.api.message_attempt_api import MessageAttemptApi
