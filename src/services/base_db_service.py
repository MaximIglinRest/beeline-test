from typing import Protocol, Type
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

import models
from db.postgres import async_session, engine
from services.exceptions import DuplicatedItemException, ItemNotFoundException


class ServiceProtocol(Protocol):
    @classmethod
    async def list(cls) -> list[BaseModel]:
        """Return list of items"""

    @classmethod
    async def retrieve(cls, item_id: UUID) -> BaseModel:
        """Retrieve item by id"""

    @classmethod
    async def create(cls, item: BaseModel) -> BaseModel:
        """Create new item"""

    async def __aenter__(self):
        """Manages db connection close before use"""

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Manages db connection close after use"""


class BaseService:
    model: Type[models.Base]
    schema: Type[BaseModel]
    primary_key: str

    @classmethod
    async def list(cls) -> list[BaseModel]:
        async with async_session() as session:
            query = select(cls.model)
            result = await session.scalars(query)
            items = result.all()
            return [cls.schema.from_orm(item) for item in items]

    @classmethod
    async def retrieve(cls, item_id: UUID) -> BaseModel:
        async with async_session() as session:
            db_item = await session.get(cls.model, item_id)
        if db_item is None:
            raise ItemNotFoundException("Not Found")
        return cls.schema.from_orm(db_item)

    @classmethod
    async def create(
        cls,
        item: BaseModel,
        *args,
        **kwargs,
    ) -> BaseModel:
        data = item.dict()
        orm_item = cls.model(**data)
        await cls._create(orm_item)
        return cls.schema.from_orm(orm_item)

    @staticmethod
    async def _create(orm_item: models.Base) -> None:
        try:
            async with async_session() as session:
                session.add(orm_item)
                await session.commit()
        except IntegrityError:
            raise DuplicatedItemException("Duplicated item")

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await engine.dispose()
