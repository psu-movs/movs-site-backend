from beanie import Document
from pydantic import BaseModel

from internal.flags import Permissions


class PartialUser(BaseModel):
    username: str
    email: str
    permissions: Permissions


class User(Document):
    username: str
    password: str | None = None
    email: str
    permissions: Permissions

    class Settings:
        name = "users"

    def has_permissions(self, permissions: Permissions) -> bool:
        return (
            permissions in self.permissions
            or Permissions.ADMINISTRATOR in self.permissions
        )
