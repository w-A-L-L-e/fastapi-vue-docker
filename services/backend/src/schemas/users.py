from tortoise.contrib.pydantic import pydantic_model_creator
from src.database.models import Users
from typing import Optional
from pydantic import BaseModel


UserInSchema = pydantic_model_creator(
    Users, name="UserIn", exclude_readonly=True, exclude=['role_id']
)
UserOutSchema = pydantic_model_creator(
    Users, name="UserOut",
    exclude=["note", "password", "created_at", "modified_at"]
)
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User", exclude=["created_at", "modified_at"]
)


class UserRoleUpdate(BaseModel):
    username: Optional[str]
    role_id: int
    # full_name: Optional[str]
    # ldap_uuid
