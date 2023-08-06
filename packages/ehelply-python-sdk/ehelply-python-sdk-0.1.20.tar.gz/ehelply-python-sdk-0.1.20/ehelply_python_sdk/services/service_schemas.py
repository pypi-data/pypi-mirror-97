from typing import Union, Callable, List, Dict, Tuple, Type, Any, TypeVar, Optional
from pydantic import BaseModel
from requests import Response


class HTTPResponse(BaseModel):
    status_code: int = 200

    def __init__(self, *args, **data: Any) -> None:
        super().__init__(**data)


class MessageResponse(HTTPResponse):
    message: str


class ErrorResponse(MessageResponse):
    pass


class ErrorHTTP401Response(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        if 'detail' in data and 'message' not in data:
            super().__init__(**data, status_code=401, message=data['detail'])
        else:
            super().__init__(**data, status_code=401)


class ErrorHTTP403Response(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        if 'detail' in data and 'message' not in data:
            super().__init__(**data, status_code=403, message=data['detail'])
        else:
            super().__init__(**data, status_code=403)


class ErrorHTTP404Response(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        if 'detail' in data and 'message' not in data:
            super().__init__(**data, status_code=404, message=data['detail'])
        else:
            super().__init__(**data, status_code=404)


class ErrorHTTP409Response(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        if 'detail' in data and 'message' not in data:
            super().__init__(**data, status_code=409, message=data['detail'])
        else:
            super().__init__(**data, status_code=409)


class ErrorHTTP422Response(ErrorResponse):
    detail: dict

    def __init__(self, **data: Any) -> None:
        super().__init__(**data, status_code=422, message="Parameters failed validation")


class ErrorHTTP500Response(ErrorResponse):
    def __init__(self, **data: Any) -> None:
        super().__init__(**data, status_code=500, message="Server Error")


GenericHTTPResponse = TypeVar('GenericHTTPResponse', bound=HTTPResponse)


def transform_response_to_schema(response: Response, schema: Union[None, Type[HTTPResponse]]) -> GenericHTTPResponse:
    if response.status_code == 200:
        if schema:
            result: Union[list, dict] = response.json()
            if isinstance(result, dict):
                return schema(**result)
            elif isinstance(result, list):
                return schema(*result)
            else:
                raise Exception("Response cannot be coerced into schema. JSON response must be a valid list or object")
        return HTTPResponse()

    if response.status_code == 403:
        return ErrorHTTP403Response(**response.json())

    if response.status_code == 404:
        return ErrorHTTP404Response(**response.json())

    if response.status_code == 409:
        return ErrorHTTP409Response(**response.json())

    if response.status_code == 422:
        return ErrorHTTP422Response(**response.json())

    if response.status_code == 500:
        return ErrorHTTP500Response()

    return ErrorResponse(message="Undefined Error - eHelply SDK might be confused", status_code=0)


def is_response_error(response: Union[Response, HTTPResponse]) -> bool:
    if response.status_code != 200:
        return True
    return False


class Pagination(BaseModel):
    """
    Pagination state
    """
    current_page: Optional[int] = None
    page_size: int = 25
    total_items: Optional[int] = None
    total_pages: Optional[int] = None
    has_previous_page: Optional[bool] = None
    has_next_page: Optional[bool] = True
    previous_page: Optional[int] = None
    next_page: Optional[int] = 1


class PageResponse(HTTPResponse):
    """
    Page state
    """
    items: list
    pagination: Pagination

    def transform(self, transformer: Callable):
        """
        Transforms results from a DB backbone into a Pydantic (or other) object type

        Args:
            transformer (Callable): A function which takes in an input and returns a transformed output

        Returns:
            None

        """
        items: list = self.items
        self.items = []
        for item in items:
            self.items.append(transformer(item))

    def transform_dict(self, pydantic_type: Type[BaseModel]):
        """
        Transforms results from a dict into a Pydantic (or other) object type

        Returns:
            None

        """
        items: list = self.items
        self.items = []
        for item in items:
            self.items.append(pydantic_type(**item))
