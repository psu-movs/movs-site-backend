from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile

from internal import auth
from internal.error import MissingPermissions
from internal.flags import Permissions
from schemas import ApplicantsCompany, User

from config import API_PREFIX
from internal.cloud_storage import ImageKitCloudStorage


router = APIRouter(prefix=API_PREFIX)


@router.get("/applicants/companies")
async def get_companies() -> list[ApplicantsCompany]:
    return await ApplicantsCompany.find_all().to_list()


@router.post("/applicants/companies")
async def add_new_company(
    image: UploadFile,
    user: Annotated[User, Depends(auth.get_current_user)],
) -> ApplicantsCompany:
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    company = ApplicantsCompany()

    await company.create()

    result = await ImageKitCloudStorage().upload_file(
        f"/applicants_companies",
        image.file,
        str(company.id)
    )
    company.image_url = result["url"]
    company.image_file_id = result["file_id"]

    await company.save()

    return company


@router.patch("/applicants/companies/{company_id}")
async def edit_company(
    company_id: str,
    user: Annotated[User, Depends(auth.get_current_user)],
    image: UploadFile | None = None,
) -> ApplicantsCompany:
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    company = await ApplicantsCompany.get(company_id)

    if image is not None:
        if company.image_file_id:
            await ImageKitCloudStorage().delete_file(company.image_file_id)

        result = await ImageKitCloudStorage().upload_file(
            f"/applicants_companies",
            image.file,
            str(company.id)
        )
        company.image_url = result["url"]
        company.image_file_id = result["file_id"]

    await company.save()

    return company


@router.delete("/applicants/companies/{company_id}")
async def delete_company(
    company_id: str,
    user: Annotated[User, Depends(auth.get_current_user)],
):
    if not user.has_permissions(Permissions.MANAGE_INFO):
        raise MissingPermissions()

    company = await ApplicantsCompany.get(company_id)
    await ImageKitCloudStorage().delete_file(company.image_file_id)
    await company.delete()
