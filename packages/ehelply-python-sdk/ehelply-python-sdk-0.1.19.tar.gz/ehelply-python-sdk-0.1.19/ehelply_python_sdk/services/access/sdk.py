from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase


class AuthModel:
    def __init__(
            self,
            access_sdk=None,
            active_participant_uuid=None,
            entity_identifier=None,
            project_uuid=None,
            access_token=None,
            secret_token=None,
            claims=None,
            data=None,
    ) -> None:
        self.access_sdk = access_sdk
        self.active_participant_uuid = active_participant_uuid
        self.entity_identifier = entity_identifier
        self.project_uuid = project_uuid
        self.access_token = access_token
        self.secret_token = secret_token
        self.claims = claims
        self.data = data


class AccessSDK(SDKBase):
    def get_base_url(self) -> str:
        partition_identifier: str = self.sdk_configuration.project_identifier
        if self.sdk_configuration.partition_identifier:
            partition_identifier = self.sdk_configuration.partition_identifier
        return super().get_base_url() + "/access/partitions/" + partition_identifier

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

    def make_partition_override(self, partition: str) -> str:
        components: List[str] = self.get_base_url().split("/")
        components.pop()
        components.append(partition)
        return "/".join(components)

    def search_types(self, name: str = None, pagination: Pagination = None) -> Union[GenericHTTPResponse, PageResponse]:
        params: dict = {}
        if name:
            params["name"] = name

        if pagination:
            params["page"] = pagination.next_page
            params["page_size"] = pagination.page_size

        response: PageResponse = transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/permissions/types",
                params=params
            ),
            schema=PageResponse
        )

        if is_response_error(response):
            return response

        response.transform_dict(pydantic_type=SearchTypeItem)

        return response

    def create_type(self, partition_type: CreateType) -> Union[GenericHTTPResponse, CreateTypeResponse]:
        """
        Parameters
        ----------
        partition_type : CreateType
            Pydantic model which defines the parameters of the type to create

        Returns
        -------

        """
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/permissions/types",
                json={"partition_type": partition_type.dict()}
            ),
            schema=CreateTypeResponse
        )

    def create_node(self, partition_type_uuid: str, node: CreateNode) -> Union[GenericHTTPResponse, CreateNodeResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/permissions/types/" + partition_type_uuid + "/nodes",
                json={"node": node.dict()}
            ),
            schema=CreateNodeResponse
        )

    def search_nodes(self, type_uuid: str, node: str = None, pagination: Pagination = None) -> Union[GenericHTTPResponse, PageResponse]:
        params: dict = {}
        if node:
            params["node"] = node

        if pagination:
            params["page"] = pagination.next_page
            params["page_size"] = pagination.page_size

        response: PageResponse = transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/permissions/types/" + type_uuid + "/nodes",
                params=params
            ),
            schema=PageResponse
        )

        if is_response_error(response):
            return response

        response.transform_dict(pydantic_type=SearchNodeItem)

        return response

    def search_group(self, pagination: Pagination = None) -> Union[GenericHTTPResponse, PageResponse]:
        params: dict = {}

        if pagination:
            params["page"] = pagination.next_page
            params["page_size"] = pagination.page_size

        response: PageResponse = transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/who/groups",
                params=params
            ),
            schema=PageResponse
        )

        if is_response_error(response):
            return response

        response.transform_dict(pydantic_type=SearchGroupItem)

        return response

    def create_group(self, group: CreateGroup) -> Union[GenericHTTPResponse, CreateGroupResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/who/groups",
                json={"group": group.dict()}
            ),
            schema=CreateGroupResponse
        )

    def create_role(self, role: CreateRole) -> Union[GenericHTTPResponse, CreateRoleResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/roles",
                json={"role": role.dict()}
            ),
            schema=CreateRoleResponse
        )

    def add_node_to_role(self, node_uuid: str, role_uuid: str) -> Union[
        GenericHTTPResponse, MessageResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/roles/" + role_uuid + "/nodes/" + node_uuid
            ),
            schema=MessageResponse
        )

    def remove_node_from_role(self, node_uuid: str, role_uuid: str) -> Union[
        GenericHTTPResponse, MessageResponse]:
        return transform_response_to_schema(
            self.requests_session.delete(
                self.get_base_url() + "/roles/" + role_uuid + "/nodes/" + node_uuid
            ),
            schema=MessageResponse
        )
    
    def add_node_to_key(self, node_uuid: str, key_uuid: str) -> Union[
        GenericHTTPResponse, MessageResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/keys/" + key_uuid + "/nodes/" + node_uuid
            ),
            schema=MessageResponse
        )

    def remove_node_from_key(self, node_uuid: str, key_uuid: str) -> Union[
        GenericHTTPResponse, MessageResponse]:
        return transform_response_to_schema(
            self.requests_session.delete(
                self.get_base_url() + "/keys/" + key_uuid + "/nodes/" + node_uuid
            ),
            schema=MessageResponse
        )

    def add_entity_to_group(self, entity_identifier: str, group_uuid: str) -> Union[
        GenericHTTPResponse, MessageResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/who/groups/" + group_uuid + "/entities/" + entity_identifier
            ),
            schema=MessageResponse
        )

    def remove_entity_from_group(self, entity_identifier: str, group_uuid: str) -> Union[
        GenericHTTPResponse, MessageResponse]:
        return transform_response_to_schema(
            self.requests_session.delete(
                self.get_base_url() + "/who/groups/" + group_uuid + "/entities/" + entity_identifier
            ),
            schema=MessageResponse
        )

    def add_key_to_entity(
            self,
            entity_identifier: str,
            key_uuid: str
    ) -> Union[GenericHTTPResponse, AddKeyToEntityResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/who/entities/" + entity_identifier + "/keys/" + key_uuid
            ),
            schema=AddKeyToEntityResponse
        )

    def remove_key_from_entity(
            self,
            entity_identifier: str,
            key_uuid: str
    ) -> Union[GenericHTTPResponse, RemoveKeyFromEntityResponse]:
        return transform_response_to_schema(
            self.requests_session.delete(
                self.get_base_url() + "/who/entities/" + entity_identifier + "/keys/" + key_uuid
            ),
            schema=RemoveKeyFromEntityResponse
        )

    def get_keys_for_entity(
            self,
            entity_identifier: str
    ) -> Union[GenericHTTPResponse, PageResponse]:
        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/who/entities/" + entity_identifier + "/keys"
            ),
            schema=PageResponse
        )

    def get_nodes_for_entity(
            self,
            entity_identifier: str
    ) -> Union[GenericHTTPResponse, GetNodesResponse]:
        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/permissions/nodes/entities/" + entity_identifier
            ),
            schema=GetNodesResponse
        )

    def get_nodes_for_entity_key(
            self,
            entity_identifier: str,
            key_uuid: str
    ) -> Union[GenericHTTPResponse, GetNodesResponse]:
        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/permissions/nodes/entities/" + entity_identifier + "/keys/" + key_uuid
            ),
            schema=GetNodesResponse
        )

    def make_rgt(
            self,
            role_uuid: str,
            group_uuid: str,
            target_identifier: str
    ) -> Union[GenericHTTPResponse, MakeRGTResponse]:
        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/rgts/roles/" + role_uuid + "/groups/" + group_uuid + "/targets/" + target_identifier,
                json={"limits": []}
            ),
            schema=MakeRGTResponse
        )

    def automate_role_group_rgt(
            self,
            role: CreateRole,
            group: CreateGroup,
            target_identifier: str,
            entity_identifiers: List[str] = None
    ) -> Union[GenericHTTPResponse, MakeRGTResponse]:

        role_response: CreateRoleResponse = self.create_role(role=role)

        if is_response_error(role_response):
            return role_response

        group_response: CreateGroupResponse = self.create_group(group=group)

        if is_response_error(group_response):
            return group_response

        if len(entity_identifiers) > 0 and not group.default:
            for entity_identifier in entity_identifiers:
                self.add_entity_to_group(entity_identifier=entity_identifier, group_uuid=group_response.uuid)

        return self.make_rgt(
            role_uuid=role_response.uuid,
            group_uuid=group_response.uuid,
            target_identifier=target_identifier
        )

    def get_entity_for_key(
            self,
            key_uuid: str,
            partition: str = None
    ) -> Union[GenericHTTPResponse, GetEntityResponse]:

        if partition:
            base_url: str = self.make_partition_override(partition=partition)
        else:
            base_url: str = self.get_base_url()

        return transform_response_to_schema(
            self.requests_session.get(
                base_url + "/who/entities/keys/" + key_uuid
            ),
            schema=GetEntityResponse
        )

    def is_entity_allowed(
            self,
            entity_identifier: str,
            target_identifier: str,
            node: str,
            partition: str = None
    ) -> bool:

        if partition:
            base_url: str = self.make_partition_override(partition=partition)
        else:
            base_url: str = self.get_base_url()

        response: Response = self.requests_session.get(
            base_url + "/auth/targets/" + target_identifier + "/nodes/" + node + "/entities/" + entity_identifier
        )

        if not is_response_error(response) and response.json() is True:
            return True

        # return transform_response_to_schema(response, None)
        return False

    # def is_key_allowed(
    #         self,
    #         access_token: str,
    #         secret_token: str,
    #         target_identifier: str,
    #         node: str,
    #         partition: str = None
    # ) -> bool:
    #     if partition:
    #         base_url: str = self.make_partition_override(partition=partition)
    #     else:
    #         base_url: str = self.get_base_url()
    #
    #     headers: dict = {
    #         "X-Access-Token": access_token,
    #         "X-Secret-Token": secret_token
    #     }
    #
    #     response: Response = self.requests_session.get(
    #         base_url + "/auth/targets/" + target_identifier + "/nodes/" + node + "/keys",
    #         headers=headers
    #     )
    #
    #     if not is_response_error(response) and response.json() is True:
    #         return True
    #
    #     # return transform_response_to_schema(response, None)
    #     return False

    def is_allowed(
            self,
            auth_model: AuthModel,
            target_identifier: str,
            node: str,
            partition: str = None
    ) -> bool:
        if auth_model.entity_identifier:
            if self.is_entity_allowed(
                    entity_identifier=auth_model.entity_identifier,
                    target_identifier=target_identifier,
                    node=node,
                    partition=partition,
            ):
                return True

        # if auth_model.access_token and auth_model.secret_token:
        #     if self.is_key_allowed(
        #             access_token=auth_model.access_token,
        #             secret_token=auth_model.secret_token,
        #             target_identifier=target_identifier,
        #             node=node,
        #             partition=partition,
        #     ):
        #         return True

        return False
