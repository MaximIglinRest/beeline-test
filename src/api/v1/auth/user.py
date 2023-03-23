from http import HTTPStatus
from typing import Union

from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

from api.v1.auth.schemas import (
    AccessTokenSchema,
    CreateUserSchema,
    ExceptionResponse,
    GetUserSchema,
    SignInUserSchema,
)
from services import AuthServiceProtocol
from services import CreateUserSchema as User
from services import (
    DuplicatedItemException,
    JWTPayload,
    UserServiceProtocol,
    get_auth_service,
    get_user_service,
)

router = InferringRouter()


@cbv(router)
class UsersCBV:
    def __init__(
        self,
        users_service: UserServiceProtocol = Depends(get_user_service),
        auth_service: AuthServiceProtocol = Depends(get_auth_service),
    ):
        self.users_service: UserServiceProtocol = users_service
        self.auth_service: AuthServiceProtocol = auth_service

    @router.post(
        "/sign-up",
        tags=["auth"],
        summary="Sign up user",
        description="Sign up user",
    )
    async def sign_up_user(
        self, user: CreateUserSchema
    ) -> Union[GetUserSchema, ExceptionResponse]:
        try:
            user = await self.users_service.create_user(User(**user.dict()))
            return GetUserSchema(**user.dict())
        except DuplicatedItemException:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=f"User {user.name} already exists",
            )

    @router.post(
        "/sign-in",
        tags=["auth"],
        summary="Sign in user",
        description="Sign up user",
    )
    async def sign_in_user(self, user: SignInUserSchema) -> AccessTokenSchema:
        user_from_db = await self.users_service.get_by_username(user.name)
        if user_from_db is not None:
            if self.users_service.verify_password(
                user.password, user_from_db.password
            ):
                return AccessTokenSchema(
                    access_token=self.auth_service.create_jwt(
                        JWTPayload(name=user_from_db.name)
                    )
                )
            else:
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="Incorrect password",
                )
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"User {user.name} doesn't exists",
        )
