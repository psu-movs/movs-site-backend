from typing import Annotated
from fastapi import APIRouter, Depends, Form, UploadFile

from config import API_PREFIX
from internal import auth
from internal.flags import Permissions
from schemas import Teacher, User
from internal.cloud_storage import ImageKitCloudStorage
from internal.error import MissingPermissions

router = APIRouter(prefix=API_PREFIX)


@router.get('/teachers')
async def get_list_teachers():
    return await Teacher.find_all().to_list()


@router.post("/teachers")
async def add_teacher(
    user: Annotated[User, Depends(auth.get_current_user)],
    first_name: Annotated[str, Form()],
    last_name: Annotated[str, Form()],
    post: Annotated[str, Form()],
    disciplines: Annotated[list[str], Form()],
    photo: UploadFile,
    surname: Annotated[str, Form()] | None = None,
    academic_degree: Annotated[str, Form()] | None = None,
):
    if not user.has_permissions(Permissions.MANAGE_TEACHERS):
        raise MissingPermissions()

    teacher = Teacher(
        first_name=first_name,
        last_name=last_name,
        surname=surname,
        post=post,
        disciplines=disciplines,
        academic_degree=academic_degree,
    )
    await teacher.insert()

    result = await ImageKitCloudStorage().upload_file(
        f"/teachers",
        photo.file,
        str(teacher.id)
    )

    teacher.photo_url = result["url"]
    teacher.photo_file_id = result["file_id"]
    await teacher.save()


@router.delete("/teachers/{teacher_id}")
async def delete_teacher(teacher_id: str, user: Annotated[User, Depends(auth.get_current_user)]):
    if not user.has_permissions(Permissions.MANAGE_TEACHERS):
        raise MissingPermissions()

    print(teacher_id)
    teacher = await Teacher.get(teacher_id)

    await ImageKitCloudStorage().delete_file(teacher.photo_file_id)
    await teacher.delete()


@router.patch("/teachers/{teacher_id}")
async def update_teacher(
    teacher_id: str,
    user: Annotated[User, Depends(auth.get_current_user)],
    first_name: Annotated[str, Form()] | None = None,
    last_name: Annotated[str, Form()] | None = None,
    post: Annotated[str, Form()] | None = None,
    disciplines: Annotated[list[str], Form()] | None = None,
    photo: UploadFile | None = None,
    surname: Annotated[str, Form()] | None = None,
    academic_degree: Annotated[str, Form()] | None = None,
):
    if not user.has_permissions(Permissions.MANAGE_TEACHERS):
        raise MissingPermissions()

    payload: dict = {k: v for k, v in locals().items() if k not in {"teacher_id", "user", "photo"} and v is not None}
    teacher = await Teacher.get(teacher_id)

    for key, value in payload.items():
        setattr(teacher, key, value)

    if photo is not None:
        await ImageKitCloudStorage().delete_file(teacher.photo_file_id)
        result = await ImageKitCloudStorage().upload_file(
            f"/teachers",
            photo.file,
            str(teacher.id)
        )
        teacher.photo_url = result["photo_url"]
        teacher.photo_file_id = result["photo_file_id"]

    await teacher.save()

