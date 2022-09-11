from typing import Optional
from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import UserRoles

# inspiration
# https://stackoverflow.com/questions/65879512/model-relationships-not-showing-in-tortoise-orm-fastapi
# https://medium.com/nerd-for-tech/python-tortoise-orm-integration-with-fastapi-c3751d248ce1

UserRoleInSchema = pydantic_model_creator(
    UserRoles, name="UserRoleIn", exclude_readonly=True)
UserRoleOutSchema = pydantic_model_creator(
    UserRoles, name="UserRole", exclude=['user'])


# class UpdateUserRole(BaseModel):
#    role: str
#    label: Optional[str]
