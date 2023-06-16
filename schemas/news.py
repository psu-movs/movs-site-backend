from beanie import Document
from pydantic import BaseModel


class Article(Document):
    author_id: str
    title: str
    creation_date: str
    description_preview: str
    description: str | None = None
    thumbnail_url: str | None = None
    thumbnail_file_id: str | None = None

    class Settings:
        name = "articles"

