from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from src.database.models import UserRoles
from src.schemas.user_roles import UserRoleOutSchema
from src.schemas.token import Status


async def get_roles():
    return await UserRoleOutSchema.from_queryset(UserRoles.all())


async def get_role(role_id) -> UserRoleOutSchema:
    return await UserRoleOutSchema.from_queryset_single(UserRoles.get(id=role_id))


async def create_role(user_role, current_user) -> UserRoleOutSchema:
    role_dict = user_role.dict(exclude_unset=True)
    # note_dict["author_id"] = current_user.id
    print("TODO check current_user.role == admin!!!!")
    print("current_user.role=", current_user.role)

    role_obj = await UserRoles.create(**role_dict)
    return await UserRoleOutSchema.from_tortoise_orm(role_obj)


async def update_role(role_id, user_role, current_user) -> UserRoleOutSchema:
    try:
        db_role = await UserRoleOutSchema.from_queryset_single(UserRoles.get(id=role_id))
    except DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"UserRole {role_id} not found")

    # TODO: check if current user is admin!
    # or better yet, put that on the routing filter ...
    # if db_note.author.id == current_user.id:
    #     await Notes.filter(id=note_id).update(**note.dict(exclude_unset=True))
    #     return await NoteOutSchema.from_queryset_single(Notes.get(id=note_id))

    # if current_user.role == ...

    await UserRoles.filter(id=role_id).update(**user_role.dict(exclude_unset=True))
    return await UserRoleOutSchema.from_queryset_single(UserRoles.get(id=role_id))

    # if not admin:
    #  raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def delete_role(role_id, current_user) -> Status:
    try:
        db_note = await UserRoleOutSchema.from_queryset_single(UserRoles.get(id=role_id))
    except DoesNotExist:
        raise HTTPException(
            status_code=404, detail=f"UserRole {role_id} not found")

    # if db_note.author.id == current_user.id:
    # if user is not admin:
    # raise HTTPException(status_code=403, detail=f"Not authorized to delete")

    deleted_count = await UserRoles.filter(id=role_id).delete()
    if not deleted_count:
        raise HTTPException(
            status_code=404, detail=f"UserRole {role_id} not found")
    return Status(message=f"Deleted user_role {role_id}")
