from functools import lru_cache
from typing import Protocol

from passlib.context import CryptContext


class BaseSecurityServiceProtocol(Protocol):
    pwd_context: CryptContext

    @classmethod
    def crypt_password(cls, password: str) -> str:
        """Function for crypt password"""
        pass

    @classmethod
    def verify_password(
        cls,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """Function for verify password from user and password from database"""
        pass


class BaseSecurityService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def crypt_password(cls, password: str) -> str:
        password = cls.pwd_context.hash(password)
        return password

    @classmethod
    def verify_password(
        cls,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)


@lru_cache()
def get_security_service() -> BaseSecurityServiceProtocol:
    return BaseSecurityService()
