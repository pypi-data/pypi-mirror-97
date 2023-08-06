from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase


class MetaSDK(SDKBase):
    def get_base_url(self) -> str:
        return super().get_base_url() + "/meta"

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

    def create_meta(
            self,
            service: str,
            type_str: str,
            entity_uuid: str,
            meta: CreateMeta
    ) -> Union[GenericHTTPResponse, CreateMetaResponse]:
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str:
            print('Invalid payload when trying to create meta.')
            return ErrorResponse(status_code=0, message="Invalid payload when trying to create meta.")

        data: dict = {
            "meta": meta.dict()
        }

        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/meta/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid,
                json=data
            ),
            schema=CreateMetaResponse
        )

    def get_meta(
            self,
            service: str,
            type_str: str,
            entity_uuid: str,
            detailed: bool = False,
            custom: bool = False,
            dates: bool = False
    ) -> Union[GenericHTTPResponse, GetMetaResponse]:
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str or type(
                detailed) is not bool or type(custom) is not bool or type(dates) is not bool:
            print('Invalid payload when trying to get meta.')
            return ErrorResponse(status_code=0, message="Invalid payload when trying to get meta.")

        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/meta/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid,
                params={"detailed": detailed, "custom": custom, "dates": dates}
            ),
            schema=GetMetaResponse
        )

    def get_meta_with_id(
            self,
            meta_id: str,
            detailed: bool = False,
            custom: bool = False,
            dates: bool = False
    ) -> Union[GenericHTTPResponse, GetMetaResponse]:
        if type(meta_id) is not str or type(detailed) is not bool or type(custom) is not bool or type(
                dates) is not bool:
            print('Invalid payload when trying to get meta.')
            return ErrorResponse(status_code=0, message="Invalid payload when trying to get meta.")

        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/meta/" + meta_id,
                params={"detailed": detailed, "custom": custom, "dates": dates}
            ),
            schema=GetMetaResponse
        )

    def update_meta(
            self,
            service: str,
            type_str: str,
            entity_uuid: str,
            meta: UpdateMeta
    ) -> Union[GenericHTTPResponse, UpdateMetaResponse]:
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str:
            print('Invalid payload when trying to update meta.')
            return ErrorResponse(status_code=0, message="Invalid payload when trying to update meta.")

        data: dict = {
            "meta": meta.dict()
        }

        return transform_response_to_schema(
            self.requests_session.put(
                self.get_base_url() + "/meta/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid,
                json=data
            ),
            schema=UpdateMetaResponse
        )

    def update_meta_with_id(
            self,
            meta_id: str,
            meta: UpdateMeta
    ) -> Union[GenericHTTPResponse, UpdateMetaResponse]:
        if type(meta_id) is not str:
            print('Invalid payload when trying to update meta.')
            return ErrorResponse(status_code=0, message="Invalid payload when trying to update meta.")

        data: dict = {
            "meta": meta.dict()
        }

        return transform_response_to_schema(
            self.requests_session.put(
                self.get_base_url() + "/meta/" + meta_id,
                json=data
            ),
            schema=UpdateMetaResponse
        )

    def delete_meta(
            self,
            service: str,
            type_str: str,
            entity_uuid: str
    ) -> Union[GenericHTTPResponse, DeleteMetaResponse]:
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str:
            print('Invalid payload when trying to delete meta.')
            return ErrorResponse(status_code=0, message="Invalid payload when trying to delete meta.")

        return transform_response_to_schema(
            self.requests_session.delete(
                self.get_base_url() + "/meta/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid,
            ),
            schema=DeleteMetaResponse
        )

    def delete_meta_with_id(
            self,
            meta_id: str
    ) -> Union[GenericHTTPResponse, DeleteMetaResponse]:
        if type(meta_id) is not str:
            print('Invalid payload when trying to delete meta.')
            return ErrorResponse(status_code=0, message="Invalid payload when trying to delete meta.")

        return transform_response_to_schema(
            self.requests_session.delete(
                self.get_base_url() + "/meta/" + meta_id,
            ),
            schema=DeleteMetaResponse
        )

    def touch_meta(
            self,
            service: str,
            type_str: str,
            entity_uuid: str
    ) -> Union[GenericHTTPResponse, TouchMetaResponse]:
        if type(service) is not str or type(type_str) is not str or type(entity_uuid) is not str:
            print('Invalid payload when trying to touch meta.')
            return ErrorResponse(status_code=0, message="Invalid payload when trying to touch meta.")

        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/meta/service/" + service + "/type/" + type_str + "/entity/" + entity_uuid + "/touch",
            ),
            schema=TouchMetaResponse
        )
