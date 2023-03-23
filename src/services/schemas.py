from uuid import UUID

from pydantic import BaseModel


class JWTPayload(BaseModel):
    name: str


class CreateUserSchema(BaseModel):
    name: str
    password: str


class GetUserSchema(BaseModel):
    id: UUID
    name: str

    class Config:
        orm_mode = True
