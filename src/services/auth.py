import time
from functools import lru_cache
from typing import Protocol

import jwt

from core.config import settings
from services.schemas import JWTPayload


class AuthServiceProtocol(Protocol):
    @staticmethod
    def create_jwt(payload: JWTPayload) -> str:
        """Create jwt from payload"""

    @staticmethod
    def decode_jwt(token: str) -> JWTPayload:
        """Get payload from jwt"""

    def verify_jwt(self, token: str) -> bool:
        """Verify jwt payload"""


class AuthService:
    @staticmethod
    def create_jwt(payload: JWTPayload) -> str:
        return jwt.encode(
            {**payload.dict(), "expire": time.time() + 600},
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

    @staticmethod
    def decode_jwt(token: str) -> JWTPayload:
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        return (
            JWTPayload.parse_obj(decoded_token)
            if decoded_token["expire"] >= time.time()
            else None
        )

    def verify_jwt(self, token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = self.decode_jwt(token)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


@lru_cache
def get_auth_service() -> AuthServiceProtocol:
    return AuthService()
