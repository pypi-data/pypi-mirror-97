from typing import Union
from pydantic import BaseModel

import requests

from ehelply_python_sdk.utils import SDKConfiguration


class SDKBase:
    """
    Provides the base class for service SDKs
    """
    def __init__(self, sdk_configuration: SDKConfiguration, requests_session: requests.Session) -> None:
        self.sdk_configuration: SDKConfiguration = sdk_configuration
        self.requests_session: requests.Session = requests_session

    def get_base_url(self) -> str:
        if self.sdk_configuration.base_url_override:
            return self.sdk_configuration.base_url_override
        else:
            return "https://api.prod.ehelply.com"

    def load(self) -> bool:
        return True

    def get_docs_url(self) -> str:
        return "Not available yet"

    def get_service_version(self) -> str:
        return ""
