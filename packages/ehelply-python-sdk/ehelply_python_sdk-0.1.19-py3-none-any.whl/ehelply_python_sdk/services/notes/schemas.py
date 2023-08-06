from ehelply_python_sdk.services.service_schemas import *


class BaseNoteMeta(BaseModel):
    original_author: Optional[str]
    author: str
    previous_version: Optional[str]
    next_version: Optional[str]


class GetNote(BaseModel):
    uuid: str
    content: str
    time: str
    meta: BaseNoteMeta


class GetNoteResponse(HTTPResponse):
    uuid: str
    content: str
    time: str
    meta: BaseNoteMeta
    history: List[GetNote] = []


class CreateNote(BaseModel):
    content: str
    time: str
    meta: BaseNoteMeta


class CreateNoteResponse(HTTPResponse):
    uuid: str
    content: str
    time: str
    meta: BaseNoteMeta


class UpdateNote(BaseModel):
    content: str
    time: str
    meta: BaseNoteMeta


class UpdateNoteResponse(HTTPResponse):
    uuid: str
    content: str
    time: str
    meta: BaseNoteMeta


class DeleteNoteResponse(MessageResponse):
    deleted_note_versions: List[str]
