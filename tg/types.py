from typing import Any
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class Type(BaseModel):
    pass


class Response(Type):
    description: str = Field("")
    error_code: int = Field(0)
    ok: bool = Field(...)
    result: Any = Field(None)


class User(Type):
    id: int = Field(...)
    is_bot: bool = Field(...)
    first_name: str = Field(...)
    last_name: str = Field("")
    username: str = Field("")


class WebhookInfo(Type):
    url: str = Field(...)
    pending_update_count: int = Field(0)
    last_error_date: int = Field(0)
    last_error_message: str = Field("")


class GetMeResponse(Response):
    result: Optional[User] = Field(None)


class GetWebhookInfoResponse(Response):
    result: Optional[WebhookInfo] = Field(None)


class SetWebhookResponse(Response):
    result: bool = Field(False)
