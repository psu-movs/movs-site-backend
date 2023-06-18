from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile

from internal import auth
from internal.error import MissingPermissions
from internal.flags import Permissions
from schemas import ScienceWork, User

from config import API_PREFIX
from internal.cloud_storage import ImageKitCloudStorage


router = APIRouter(prefix=API_PREFIX)


@router.get("/science_works")
async def get_science_works() -> list[ScienceWork]:
    works = await ScienceWork.find_all().to_list()
    return [work.dict(exclude={"description"}) for work in works[::-1]]


@router.get("/science_works/{science_work_id}")
async def get_science_work(science_work_id: str) -> ScienceWork:
    return await ScienceWork.get(science_work_id)


@router.post("/science_works")
async def add_new_science_work(
    title: Annotated[str, Form()],
    description: Annotated[str, Form()],
    image: UploadFile,
    user: Annotated[User, Depends(auth.get_current_user)],
) -> ScienceWork:
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    science_work = ScienceWork(
        title=title,
        description=description,
    )

    await science_work.create()

    result = await ImageKitCloudStorage().upload_file(
        f"/science_works",
        image.file,
        str(science_work.id)
    )
    science_work.image_url = result["url"]
    science_work.image_file_id = result["file_id"]

    await science_work.save()

    return science_work


@router.patch("/science_works/{science_work_id}")
async def edit_science_work(
    science_work_id: str,
    user: Annotated[User, Depends(auth.get_current_user)],
    title: str = Form(None),
    description: str = Form(None),
    image: UploadFile | None = None,
) -> ScienceWork:
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    science_work = await ScienceWork.get(science_work_id)

    if title is not None:
        science_work.title = title
    if description is not None:
        science_work.description = description

    if image is not None:
        if science_work.image_file_id:
            await ImageKitCloudStorage().delete_file(science_work.image_file_id)

        result = await ImageKitCloudStorage().upload_file(
            f"/science_works",
            image.file,
            str(science_work.id)
        )
        science_work.image_url = result["url"]
        science_work.image_file_id = result["file_id"]

    await science_work.save()

    return science_work


@router.delete("/science_works/{science_work_id}")
async def delete_science_work(
    science_work_id: str,
    user: Annotated[User, Depends(auth.get_current_user)],
):
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    science_work = await ScienceWork.get(science_work_id)
    await ImageKitCloudStorage().delete_file(science_work.image_file_id)
    await science_work.delete()
