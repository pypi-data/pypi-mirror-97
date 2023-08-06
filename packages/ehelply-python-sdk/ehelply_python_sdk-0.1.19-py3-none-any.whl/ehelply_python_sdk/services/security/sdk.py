from typing import Union

from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase


class SecuritySDK(SDKBase):
    def get_base_url(self) -> str:
        return super().get_base_url() + "/security"

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

    def create_token(self, length: int = 64) -> Union[GenericHTTPResponse, CreateTokenResponse]:
        response = self.requests_session.post(
            self.get_base_url() + "/tokens",
            json={"token": {"length": length}}
        )

        if is_response_error(response):
            return transform_response_to_schema(response, None)

        return CreateTokenResponse(
            token=response.json()
        )

    def create_key(self, key: CreateKey, access_length: int = 48, secret_length: int = 48) -> Union[CreateKeyResponse, GenericHTTPResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/keys",
                json={"key": key.dict()},
                params={"secret_length": secret_length, "access_length": access_length}
            ),
            schema=CreateKeyResponse
        )

    def verify_key(self, access: str, secret: str) -> Union[GenericHTTPResponse, VerifyKeyResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/keys/verify",
                json={
                    "key": {
                        "access": access,
                        "secret": secret
                    }
                }
            ),
            schema=VerifyKeyResponse
        )
