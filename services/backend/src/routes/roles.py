from typing import List

from fastapi import APIRouter, Depends, HTTPException
from tortoise.contrib.fastapi import HTTPNotFoundError
from tortoise.exceptions import DoesNotExist

import src.crud.user_roles as crud
from src.auth.jwthandler import get_current_user
# from src.schemas.notes import NoteOutSchema, NoteInSchema, UpdateNote
from src.schemas.user_roles import UserRoleInSchema, UserRoleOutSchema  # , UpdateUserRole
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


router = APIRouter()


@router.get(
    "/roles",
    response_model=List[UserRoleOutSchema],
    dependencies=[Depends(get_current_user)],
)
async def get_user_roles():
    return await crud.get_roles()


@router.get(
    "/roles/{role_id}",
    response_model=UserRoleOutSchema,
    dependencies=[Depends(get_current_user)],
)
async def get_role(role_id: int) -> UserRoleOutSchema:
    try:
        return await crud.get_role(role_id)
    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail="UserRole does not exist",
        )


@router.post(
    "/roles", response_model=UserRoleOutSchema, dependencies=[Depends(get_current_user)]
)
async def create_role(
    user_role: UserRoleInSchema, current_user: UserOutSchema = Depends(get_current_user)
) -> UserRoleOutSchema:
    return await crud.create_role(user_role, current_user)


@router.patch(
    "/roles/{role_id}",
    dependencies=[Depends(get_current_user)],
    response_model=UserRoleOutSchema,
    responses={404: {"model": HTTPNotFoundError}},
)
async def update_role(
    role_id: int,
    role: UserRoleInSchema,  # or we can use UpdateUserRole
    current_user: UserOutSchema = Depends(get_current_user),
) -> UserRoleOutSchema:
    return await crud.update_role(role_id, role, current_user)


@router.delete(
    "/roles/{role_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}},
    dependencies=[Depends(get_current_user)],
)
async def delete_role(
    role_id: int, current_user: UserOutSchema = Depends(get_current_user)
):
    return await crud.delete_role(role_id, current_user)
