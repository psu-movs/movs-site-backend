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


class BaseContent(BaseModel):
    type: TextContentType
    "Тип контента"
    meta: dict | None = None
    "Дополнительная информация"


class TextContent(BaseContent):
    type: TextContentType = TextContentType.TEXT
    content: str
    "Текст контента"


class ImageContent(BaseContent):
    type: TextContentType = TextContentType.IMAGE
    image: Image
    "Изображение"


class TextContentWithImage(BaseContent):
    type: TextContentType = TextContentType.TEXT_WITH_IMAGE
    content: str
    "Текст контента"
    image: Image
    "Изображение"



