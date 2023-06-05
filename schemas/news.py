from beanie import Document


class Article(Document):
    author_id: str
    title: str
    description: str
    creation_date: str
    thumbnail_url: str | None = None
    thumbnail_file_id: str | None = None

