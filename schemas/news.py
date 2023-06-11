from beanie import Document
from pydantic import BaseModel


class Article(Document):
    author_id: str
    title: str
    description: str | None = None
    creation_date: str
    thumbnail_url: str | None = None
    thumbnail_file_id: str | None = None

    class Settings:
        name = "articles"

