import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile

from internal import auth
from internal.error import MissingPermissions
from internal.flags import Permissions
from schemas import Article, User

from config import API_PREFIX
from internal.cloud_storage import ImageKitCloudStorage


router = APIRouter(prefix=API_PREFIX)


@router.get("/news")
async def get_news() -> list[Article]:
    articles = await Article.find_all().to_list()
    return [article.dict(exclude={"description"}) for article in articles]


@router.get("/news/{article_id}")
async def get_article(article_id: str):
    return await Article.get(article_id)


@router.post("/news")
async def add_new_article(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    thumbnail: UploadFile,
    user: Annotated[User, Depends(auth.get_current_user)],
) -> Article:
    if not user.has_permissions(Permissions.MANAGE_NEWS):
        raise MissingPermissions()

    creation_date = datetime.datetime.now(datetime.timezone.utc).isoformat()
    article = Article(
        author_id=str(user.id),
        title=title,
        description=description,
        creation_date=creation_date
    )

    await article.create()

    result = await ImageKitCloudStorage().upload_file(
        f"/department_head",
        thumbnail.file,
        str(article.id)
    )
    article.thumbnail_url = result["url"]
    article.thumbnail_file_id = result["file_id"]

    await article.save()

    return article


@router.patch("/news/{article_id}")
async def edit_article(
    article_id: str,
    user: Annotated[User, Depends(auth.get_current_user)],
    title: Annotated[str, Form()] | None = None,
    description: Annotated[str, Form()] | None = None,
    thumbnail: UploadFile | None = None,
) -> Article:
    if not user.has_permissions(Permissions.MANAGE_NEWS):
        raise MissingPermissions()

    article = await Article.get(article_id)

    if title is not None:
        article.title = title
    if description is not None:
        article.description = description

    if article.thumbnail_file_id:
        await ImageKitCloudStorage().delete_file(article.thumbnail_file_id)

    result = await ImageKitCloudStorage().upload_file(
        f"/department_head",
        thumbnail.file,
        str(article.id)
    )
    article.thumbnail_url = result["url"]
    article.thumbnail_file_id = result["file_id"]

    await article.save()

    return article


@router.delete("/news/{article_id}")
async def delete_article(
    article_id: str,
    user: Annotated[User, Depends(auth.get_current_user)],
):
    if not user.has_permissions(Permissions.MANAGE_NEWS):
        raise MissingPermissions()

    article = await Article.get(article_id)
    await article.delete()