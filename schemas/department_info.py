from beanie import Document
from pydantic import BaseModel


class OptionalContacts(BaseModel):
    phone: str | None = None
    email: str | None = None
    address: str | None = None


class Contacts(Document):
    phone: str
    email: str
    address: str


class DepartmentHead(Contacts):
    full_name: str
    post: str
    photo_url: str | None = None
    photo_file_id: str | None = None


class PartialDepartmentInfo(OptionalContacts):
    description: str | None = None


class DepartmentInfo(Contacts):
    description: str
