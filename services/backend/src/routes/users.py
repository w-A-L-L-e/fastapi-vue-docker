from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from tortoise.contrib.fastapi import HTTPNotFoundError

import src.crud.users as crud
from src.auth.users import validate_user
from src.schemas.token import Status
from src.schemas.users import UserInSchema, UserOutSchema, UserRoleUpdate 

from src.auth.jwthandler import (
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


router = APIRouter()


@router.post("/register", response_model=UserOutSchema)
async def create_user(user: UserInSchema) -> UserOutSchema:
    return await crud.create_user(user)


@router.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends()):
    user = await validate_user(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_role = "unconfigured_user"
    if user.role:
        user_role = user.role.role
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.username,
            "role": user_role
        },
        expires_delta=access_token_expires
    )
    token = jsonable_encoder(access_token)
    content = {"message": "You've successfully logged in. Welcome back!"}
    response = JSONResponse(content=content)
    response.set_cookie(
        "Authorization",
        value=f"Bearer {token}",
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES*60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES*60,
        samesite="Lax",
        secure=False,
    )

    return response


@router.get(
    "/users/whoami",
    response_model=UserOutSchema,
    dependencies=[Depends(get_current_user)]
)
async def read_users_me(
    current_user: UserOutSchema = Depends(get_current_user)
):
    return current_user


@router.delete(
    "/user/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_user(
    user_id: int, current_user: UserOutSchema = Depends(get_current_user)
) -> Status:
    return await crud.delete_user(user_id, current_user)


@router.get(
    "/users",
    response_model=List[UserOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_users(
    current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.get_users(current_user)


@router.patch(
    "/users/{user_id}/update_role",
    dependencies=[Depends(get_current_user)],
    response_model=UserOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_user_role(
    user_id: int,
    user: UserRoleUpdate,
    current_user: UserOutSchema = Depends(get_current_user),
) -> UserOutSchema:
    return await crud.update_user_role(user_id, user, current_user)



