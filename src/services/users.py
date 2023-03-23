from typing import Optional, Protocol

from fastapi import Depends
from sqlalchemy import select

import models
from db.postgres import get_async_session
from services.auth import AuthServiceProtocol, get_auth_service
from services.base_db_service import BaseService
from services.schemas import CreateUserSchema, GetUserSchema
from services.security import BaseSecurityServiceProtocol, get_security_service


class UserServiceProtocol(Protocol):
    async def create_user(self, user: CreateUserSchema) -> GetUserSchema:
        """Create user and save to database"""

    async def get_by_username(self, username) -> Optional[GetUserSchema]:
        """Get user from database by username"""

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """Verify incoming password with password in database"""


class UserService(BaseService):
    model = models.User
    schema = GetUserSchema

    def __init__(
        self,
        session,
        security_service: BaseSecurityServiceProtocol,
        auth_service: AuthServiceProtocol,
    ):
        self.session = session
        self.security_service = security_service
        self.auth_service = auth_service

    async def create_user(self, user: CreateUserSchema) -> GetUserSchema:
        user.password = self.security_service.crypt_password(user.password)
        orm_item = self.model(**user.dict())
        await self._create(orm_item)
        return self.schema.from_orm(orm_item)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return self.security_service.verify_password(
            plain_password,
            hashed_password,
        )

    async def get_by_username(self, username: str) -> Optional[GetUserSchema]:
        async with self.session() as session:
            query = select(self.model).where(self.model.name == username)
            users = await session.scalars(query)
            return users.first()


def get_user_service(
    session=Depends(get_async_session),
    security_service: BaseSecurityServiceProtocol = Depends(
        get_security_service
    ),
    auth_service: AuthServiceProtocol = Depends(get_auth_service),
) -> UserServiceProtocol:
    return UserService(session, security_service, auth_service)
