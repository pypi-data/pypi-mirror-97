from .openapi_client import ApiClient, Configuration

class Diahook():
    _configuration: Configuration
    authentication: Authentication
    application: Application
    endpoint: Endpoint
    message: Message
    message_attempt: MessageAttempt

    def __init__(self, ) -> None:
        pass
