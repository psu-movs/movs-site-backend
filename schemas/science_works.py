from beanie import Document
from pydantic import BaseModel


class ScienceWork(Document):
    title: str
    description: str
    image_url: str | None = None
    image_file_id: str | None = None

    class Settings:
        name = "science_works"

