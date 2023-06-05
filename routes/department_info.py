from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile

from config import API_PREFIX
from internal import auth
from internal.cloud_storage import ImageKitCloudStorage
from internal.error import MissingPermissions, DepartmentInfoDoesNotExists, DepartmentHeadDoesNotExists
from internal.flags import Permissions
from schemas import DepartmentInfo, User
from schemas.department_info import DepartmentHead, PartialDepartmentInfo

router = APIRouter(prefix=API_PREFIX)


@router.get("/department")
async def get_department_info() -> DepartmentInfo:
    department = await DepartmentInfo.find_one()
    if department is None:
        raise DepartmentInfoDoesNotExists
    return department


@router.post("/department")
async def set_department_info(
    user: Annotated[User, Depends(auth.get_current_user)],
    department: DepartmentInfo,
) -> DepartmentInfo:
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    await department.create()
    return department


@router.patch("/department")
async def update_department_info(
    user: Annotated[User, Depends(auth.get_current_user)],
    partial_info: PartialDepartmentInfo
) -> PartialDepartmentInfo:
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    department = await DepartmentInfo.find_one()
    if department is None:
        raise DepartmentInfoDoesNotExists

    if partial_info.phone is not None:
        department.phone = partial_info.phone
    if partial_info.email is not None:
        department.email = partial_info.email
    if partial_info.address is not None:
        department.address = partial_info.address
    if partial_info.description is not None:
        department.description = partial_info.description

    await department.save()

    return department.dict(exclude={"head"})


@router.get("/department/head")
async def get_department_head() -> DepartmentHead:
    head = await DepartmentHead.find_one()
    if head is None:
        raise DepartmentHeadDoesNotExists()

    return head


@router.post("/department/head")
async def add_department_head(
    user: Annotated[User, Depends(auth.get_current_user)],
    full_name: Annotated[str, Form()],
    phone: Annotated[str, Form()],
    email: Annotated[str, Form()],
    address: Annotated[str, Form()],
    photo: UploadFile,
) -> DepartmentHead:
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    data = {k: v for k, v in locals().items() if k not in {"photo", "user"} and v is not None}
    head = DepartmentHead(**data)

    result = await ImageKitCloudStorage().upload_file(
        f"/department_head",
        photo.file,
        str(head.id)
    )
    head.photo_url = result["url"]
    head.photo_file_id = result["file_id"]

    await head.create()

    return head


@router.patch("/department/head")
async def update_department_head(
    user: Annotated[User, Depends(auth.get_current_user)],
    full_name: Annotated[str, Form()] | None = None,
    phone: Annotated[str, Form()] | None = None,
    email: Annotated[str, Form()] | None = None,
    address: Annotated[str, Form()] | None = None,
    photo: UploadFile | None = None,
) -> DepartmentHead:
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    current_head = await DepartmentHead.find_one()
    if current_head is None:
        raise DepartmentHeadDoesNotExists()

    data = {k: v for k, v in locals().items() if k not in {"photo", "user"} and v is not None}
    for attr, value in data.items():
        setattr(current_head, attr, value)

    if photo is not None:
        if current_head.photo_file_id:
            await ImageKitCloudStorage().delete_file(current_head.photo_file_id)

        result = await ImageKitCloudStorage().upload_file(
            f"/department_head",
            photo.file,
            str(current_head.id)
        )
        current_head.photo_url = result["url"]
        current_head.photo_file_id = result["file_id"]

    await current_head.save()

    return current_head
