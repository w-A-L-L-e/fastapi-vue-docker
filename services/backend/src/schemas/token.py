from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = 'user'  # uauthorized_user, admin, moderator


class Status(BaseModel):
    message: str
