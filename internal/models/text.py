# Изначально планировалось для информации о кафедре,
# но из-за того, что мы не успеваем реализовать это со стороны фронтенда,
# то эти классы более не будут использоваться (наверн /shrug)

from enum import IntEnum

from pydantic import BaseModel


class Image(BaseModel):
    """
    Объект изображения
    """

    url: str
    "Ссылка на изображение"
    label: str
    "Надпись изображения"


class TextContentType(IntEnum):
    """
    Типы контента
    """

    TEXT = 0
    "Только текст"
    IMAGE = 1
    "Только изображение"
    TEXT_WITH_IMAGE = 2
    "Текст с изображением"


class Content(BaseModel):
    type: TextContentType
    "Тип контента"
    meta: str | None = None
    "Дополнительная информация"
    content: str | None = None
    "Текст контента"
    image: Image | None = None
    "Изображение"
