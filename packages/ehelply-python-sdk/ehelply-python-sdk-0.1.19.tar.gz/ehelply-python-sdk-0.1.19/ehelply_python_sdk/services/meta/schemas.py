from ehelply_python_sdk.services.service_schemas import *


class BaseBasicMeta(BaseModel):
    """
    Basic meta
    """
    name: Optional[str]
    slug: Optional[str]


class BaseDetailedMeta(BaseModel):
    """
    Detailed meta based on Notes
    """
    summary: Optional[str]
    description: Optional[str]
    summary_history: List[str] = []
    description_history: List[str] = []


class BaseDatesMeta(BaseModel):
    """
    Date based meta
    """
    created_at: Optional[str]
    updated_at: Optional[str]


class GetMetaResponse(HTTPResponse):
    uuid: str
    basic: BaseBasicMeta = BaseBasicMeta()
    detailed: BaseDetailedMeta = BaseDetailedMeta()
    custom: dict = {}
    dates: BaseDatesMeta = BaseDatesMeta()


class BaseBasicMetaCreate(BaseModel):
    """
    Basic meta
    """
    name: Optional[str] = None
    slug: bool = True


class BaseDetailedMetaCreate(BaseModel):
    """
    Detailed meta based on Notes
    """
    summary: Optional[str] = None
    description: Optional[str] = None


class CreateMeta(BaseModel):
    basic: Optional[BaseBasicMetaCreate] = BaseBasicMetaCreate()
    detailed: Optional[BaseDetailedMetaCreate] = BaseDetailedMetaCreate()
    custom: Optional[dict] = None


class BaseDetailedMetaReturn(BaseModel):
    """
    Detailed meta based on Notes
    """
    summary_uuid: Optional[str] = None
    description_uuid: Optional[str] = None


class CreateMetaResponse(HTTPResponse):
    uuid: str
    basic: BaseBasicMeta
    detailed: BaseDetailedMetaReturn
    custom: dict = {}
    dates: BaseDatesMeta = BaseDatesMeta()


class UpdateMeta(BaseModel):
    basic: Optional[BaseBasicMetaCreate] = BaseBasicMetaCreate()
    detailed: Optional[BaseDetailedMetaCreate] = BaseDetailedMetaCreate()
    custom: Optional[dict] = None


class UpdateMetaResponse(HTTPResponse):
    uuid: str
    basic: BaseBasicMeta
    detailed: BaseDetailedMetaReturn
    custom: dict = {}
    dates: BaseDatesMeta = BaseDatesMeta()


class DeleteMetaResponse(MessageResponse):
    pass


class TouchMetaResponse(HTTPResponse):
    uuid: str
    basic: BaseBasicMeta
    detailed: BaseDetailedMetaReturn
    custom: dict = {}
    dates: BaseDatesMeta = BaseDatesMeta()
