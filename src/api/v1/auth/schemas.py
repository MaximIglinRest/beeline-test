from uuid import UUID

from pydantic import BaseModel


class ExceptionResponse(BaseModel):
    detail: str


class CreateUserSchema(BaseModel):
    name: str
    password: str


class SignInUserSchema(BaseModel):
    name: str
    password: str


class GetUserSchema(BaseModel):
    id: UUID
    name: str


class AccessTokenSchema(BaseModel):
    access_token: str
