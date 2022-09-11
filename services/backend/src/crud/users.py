from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist, IntegrityError

from src.database.models import Users
from src.schemas.token import Status
from src.schemas.users import UserOutSchema


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def is_admin(current_user):
    current_role = ''
    if current_user.role:
        current_role = current_user.role.role

    return current_role == 'admin'


async def get_users(current_user) -> UserOutSchema:
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Not authorized")
        return

    # show newest users on top
    return await UserOutSchema.from_queryset(
        Users.all().order_by('-created_at')  # - means descending
    )


async def create_user(user) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.password)

    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(
            status_code=401, detail=f"Sorry, that username already exists.")

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user) -> Status:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(
                status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail="Not authorized to delete")


async def update_user_role(user_id, user, current_user) -> UserOutSchema:
    try:
        db_user = await UserOutSchema.from_queryset_single(
            Users.get(id=user_id)
        )

    except DoesNotExist:
        raise HTTPException(
            status_code=404,
            detail=f"User {user_id} not found"
        )

    if not is_admin(current_user):
        raise HTTPException(
            status_code=403, detail="Only admin is allowed to update user roles")
        return

    user_update = user.dict(exclude_unset=True)
    await Users.filter(id=user_id).update(
        **user_update
    )
    return await UserOutSchema.from_queryset_single(Users.get(id=user_id))

    raise HTTPException(status_code=403, detail="Not authorized to update")


# TODO: update user call
# if db_user.id == current_user.id:
#     user_update = user.dict(exclude_unset=True)
