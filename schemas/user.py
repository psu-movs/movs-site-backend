from beanie import Document

from internal.flags import Permissions


class User(Document):
    full_name: str
    password: str
    email: str
    permissions: Permissions

    class Settings:
        name = "users"

    def has_permissions(self, permissions: Permissions) -> bool:
        return permissions in self.permissions