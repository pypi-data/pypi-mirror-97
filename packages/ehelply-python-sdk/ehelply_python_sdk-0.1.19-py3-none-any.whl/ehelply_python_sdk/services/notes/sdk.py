from .schemas import *
from ehelply_python_sdk.services.service_sdk_base import SDKBase
from datetime import datetime


class NotesSDK(SDKBase):
    def get_base_url(self) -> str:
        return super().get_base_url() + "/notes"

    def get_docs_url(self) -> str:
        return super().get_docs_url()

    def get_service_version(self) -> str:
        return super().get_service_version()

    def get_note(
            self,
            note_id: str,
            history: int = 0,
            history_content: bool = True
    ) -> Union[GenericHTTPResponse, GetNoteResponse]:
        return transform_response_to_schema(
            self.requests_session.get(
                self.get_base_url() + "/notes/" + note_id,
                params={"history": history, "history_content": history_content}
            ),
            schema=GetNoteResponse
        )

    def delete_note(
            self,
            note_id: str,
            method: str = "previous"
    ) -> Union[GenericHTTPResponse, DeleteNoteResponse]:
        return transform_response_to_schema(
            self.requests_session.delete(
                self.get_base_url() + "/notes/" + note_id,
                params={"method": method}
            ),
            schema=DeleteNoteResponse
        )

    def update_note(
            self,
            note_id: str,
            content: str,
            author: str,
    ) -> Union[GenericHTTPResponse, UpdateNoteResponse]:
        if type(content) is not str or type(author) is not str or type(note_id) is not str:
            print('Note entry discarded due to invalid payload.')
            return ErrorResponse(status_code=0, message="Note entry discarded due to invalid payload.")

        data: dict = {
            "note": {
                "content": content,
                "time": datetime.utcnow().isoformat(),
                "meta": {
                    "author": author,
                }
            }
        }

        return transform_response_to_schema(
            self.requests_session.put(
                self.get_base_url() + "/notes/" + note_id,
                json=data
            ),
            schema=UpdateNoteResponse
        )

    def create_note(
            self,
            content: str,
            author: str
    ) -> Union[GenericHTTPResponse, CreateNoteResponse]:
        if type(content) is not str or type(author) is not str:
            print('Note entry discarded due to invalid payload.')
            return ErrorResponse(status_code=0, message="Note entry discarded due to invalid payload.")

        data: dict = {
            "note": {
                "content": content,
                "time": datetime.utcnow().isoformat(),
                "meta": {
                    "original_author": author,
                    "author": author,
                }
            }
        }

        return transform_response_to_schema(
            self.requests_session.post(
                self.get_base_url() + "/notes",
                json=data
            ),
            schema=CreateNoteResponse
        )
