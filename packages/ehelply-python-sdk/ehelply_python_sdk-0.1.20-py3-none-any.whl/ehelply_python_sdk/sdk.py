from typing import Union, Type, TypeVar

import requests

from ehelply_python_sdk.utils import SDKConfiguration, make_requests
from ehelply_python_sdk.services import services
from ehelply_python_sdk.services.service_schemas import is_response_error, ErrorResponse

genericSDKBase = TypeVar('genericSDKBase', bound=services.SDKBase)

CONST_CLIENT_ACCESS: str = "access"
CONST_CLIENT_SECURITY: str = "security"
CONST_CLIENT_NOTES: str = "notes"
CONST_CLIENT_META: str = "meta"


class eHelplySDK:
    """
    eHelply SDK
    """
    def __init__(self, sdk_configuration: SDKConfiguration) -> None:
        self.sdk_configuration: SDKConfiguration = sdk_configuration
        self.requests_session: requests.Session = make_requests(sdk_configuration=sdk_configuration)

    def _make_client(
            self,
            client: str,
            sdk_configuration: SDKConfiguration = None,
            request_session: requests.Session = None
    ) -> genericSDKBase:
        if not sdk_configuration:
            sdk_configuration = self.sdk_configuration

        if not request_session:
            request_session = self.requests_session

        if client == CONST_CLIENT_ACCESS:
            return services.AccessSDK(sdk_configuration=sdk_configuration, requests_session=request_session)

        if client == CONST_CLIENT_SECURITY:
            return services.SecuritySDK(sdk_configuration=sdk_configuration, requests_session=request_session)
        
        if client == CONST_CLIENT_NOTES:
            return services.NotesSDK(sdk_configuration=sdk_configuration, requests_session=request_session)

        if client == CONST_CLIENT_META:
            return services.MetaSDK(sdk_configuration=sdk_configuration, requests_session=request_session)

    def make_access(
            self,
            sdk_configuration: SDKConfiguration = None,
            request_session: requests.Session = None
    ) -> services.AccessSDK:
        return self._make_client(
            client=CONST_CLIENT_ACCESS,
            sdk_configuration=sdk_configuration,
            request_session=request_session
        )

    def make_security(
            self,
            sdk_configuration: SDKConfiguration = None,
            request_session: requests.Session = None
    ) -> services.SecuritySDK:
        return self._make_client(
            client=CONST_CLIENT_SECURITY,
            sdk_configuration=sdk_configuration,
            request_session=request_session
        )
    
    def make_notes(
            self,
            sdk_configuration: SDKConfiguration = None,
            request_session: requests.Session = None
    ) -> services.NotesSDK:
        return self._make_client(
            client=CONST_CLIENT_NOTES,
            sdk_configuration=sdk_configuration,
            request_session=request_session
        )

    def make_meta(
            self,
            sdk_configuration: SDKConfiguration = None,
            request_session: requests.Session = None
    ) -> services.MetaSDK:
        return self._make_client(
            client=CONST_CLIENT_META,
            sdk_configuration=sdk_configuration,
            request_session=request_session
        )
