from ehelply_python_sdk.services.service_schemas import *


class SearchTypeItem(BaseModel):
    uuid: str
    name: str
    slug: str
    summary: str
    created_at: str


class CreateType(BaseModel):
    name: str
    summary: str


class CreateTypeResponse(HTTPResponse):
    uuid: str
    partition_identifier: str
    name: str
    slug: str
    summary: str
    created_at: str


class SearchNodeItem(BaseModel):
    uuid: str
    name: str
    node: str
    type_uuid: str
    summary: str
    created_at: str
    roles: list


class CreateNode(BaseModel):
    name: str
    node: str
    summary: str


class CreateNodeResponse(HTTPResponse):
    uuid: str
    name: str
    node: str
    type_uuid: str
    summary: str
    created_at: str


class SearchGroupItem(BaseModel):
    uuid: str
    name: str
    summary: str
    created_at: str
    default: bool


class CreateGroup(BaseModel):
    name: str
    summary: str
    entity_identifiers: List[str] = []
    default: bool = False


class CreateGroupResponse(HTTPResponse):
    uuid: str
    partition_identifier: str
    name: str
    summary: str
    created_at: str
    default: bool


class CreateRole(BaseModel):
    name: str
    summary: str


class CreateRoleResponse(HTTPResponse):
    uuid: str
    partition_identifier: str
    name: str
    summary: str
    created_at: str


class AddKeyToEntityResponse(HTTPResponse):
    entity_key_uuid: str
    key_uuid: str


class RemoveKeyFromEntityResponse(HTTPResponse):
    entity_key_uuid: str
    key_uuid: str


class MakeRGTResponse(MessageResponse):
    group_uuid: str
    target_identifier: str
    role_uuid: str


class GetEntityResponse(HTTPResponse):
    entity_identifier: str


class GetNodesResponse(HTTPResponse):
    nodes: List[SearchNodeItem]

    def __init__(self, *args, **data: Any) -> None:
        nodes: List[SearchNodeItem] = []

        for arg_node in args:
            nodes.append(SearchNodeItem(**arg_node))

        super().__init__(*args, **data, nodes=nodes)

