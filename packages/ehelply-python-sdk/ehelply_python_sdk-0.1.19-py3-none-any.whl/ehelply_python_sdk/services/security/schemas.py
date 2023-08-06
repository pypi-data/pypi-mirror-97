from ehelply_python_sdk.services.service_schemas import *


class CreateKey(BaseModel):
    name: str
    summary: str


class CreateKeyResponse(HTTPResponse):
    uuid: str
    access: str
    secret: str


class VerifyKeyResponse(HTTPResponse):
    uuid: str
    access: str
    name: str
    summary: str
    created_at: str
    last_used_at: str


class CreateTokenResponse(HTTPResponse):
    token: str
