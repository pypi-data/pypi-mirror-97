import os

from .agilicus_api.api_client import ApiClient
from .agilicus_api.configuration import Configuration


class _ApiClientWrapper(ApiClient):
    def __init__(self, configuration: Configuration = None, **kwargs):
        if not configuration:
            configuration = Configuration()

        cert_path = os.environ.get("SSL_CERT_FILE")
        if cert_path and not configuration.ssl_ca_cert:
            configuration.ssl_ca_cert = cert_path

        super().__init__(configuration=configuration, **kwargs)


def patched_api_client():
    return _ApiClientWrapper
