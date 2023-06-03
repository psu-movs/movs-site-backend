from beanie import Document


class Teacher(Document):
    first_name: str
    last_name: str
    surname: str | None
    post: str
    disciplines: list[str]
    academic_degree: str | None
    photo_url: str | None = None
    photo_file_id: str | None = None

    class Settings:
        name = "teachers"
