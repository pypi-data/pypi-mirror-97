from ehelply_python_sdk.services.service_schemas import *


class GetProjectResponse(HTTPResponse):
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    is_spend_maxed: bool


class UpdateProject(BaseModel):
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth


class UpdateProjectResponse(HTTPResponse):
    uuid: str
    name: str
    created_at: str
    current_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    max_spend: int  # Dollar formats represented by a x10000000 integer. Precision to the millonth
    is_spend_maxed: bool
    group_m_p: str  # Group UUID that joins members to partition/project
    group_p_c: str  # Group UUID that joins partition/project to eHelply Cloud
