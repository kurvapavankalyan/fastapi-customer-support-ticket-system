from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field
)


class UserInput(BaseModel):
    name: Annotated[str, BeforeValidator(lambda value: value.strip().lower())]
    password: str = Field(min_length=8, max_length=72)
    email: EmailStr


class TicketInput(BaseModel):
    message: str = Field(min_length=1)


class TicketUpdate(BaseModel):
    message: str | None = Field(default=None, min_length=1)


class AdminTicketUpdate(BaseModel):
    category: str | None = None
    priority: str | None = None
    sentiment: str | None = None
    status: str | None = None
    reply: str | None = None


class Response(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int
    name: str
    role: str


class TicketResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    ID: int
    user_id: int
    message: str
    category: str
    priority: str
    sentiment: str
    status: str
    reply: str
