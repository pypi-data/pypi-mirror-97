from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase


class MonitorSDK(SDKBase):
    def get_base_url(self) -> str:
        return super().get_base_url() + "/monitors"

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

    def get_project(
            self,
            project_uuid: str
    ) -> Union[GenericHTTPResponse, GetProjectResponse]:
        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/projects/projects/" + project_uuid
            ),
            schema=GetProjectResponse
        )
