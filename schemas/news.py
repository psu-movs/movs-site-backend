from beanie import Document
from pydantic import BaseModel

class ArticleWithoutDescription(BaseModel):
    author_id: str
    title: str
    creation_date: str
    thumbnail_url: str
    thumbnail_file_id: str

class Article(Document):
    author_id: str
    title: str
    description: str
    creation_date: str
    thumbnail_url: str | None = None
    thumbnail_file_id: str | None = None

    class Settings:
        name = "articles"

