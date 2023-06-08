from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm

from internal import auth, error
from config import API_PREFIX
from internal.flags import Permissions

from schemas.user import User
router = APIRouter(prefix=API_PREFIX)


async def authenticate_user(username: str, password: str):
    user = await User.find_one(User.email == username)
    if not user:
        return

    if not auth.verify_hashed_value(password, user.password):
        return

    return user


@router.post("/users/login")
async def authorize_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await authenticate_user(form_data.username, form_data.password)

    if user is None:
        raise error.InvalidUserData()

    access_token = auth.create_access_token(
        data={"sub": user.email}
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me")
async def get_current_user(user: Annotated[User, Depends(auth.get_current_user)]) -> User:
    return user.dict(exclude={"id", "password"})


@router.post("/users")
async def register(full_name: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()]):
    email_user = await User.find_one(User.email == email)
    name_user = await User.find_one(User.full_name == full_name)
    if email_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с такой почтой уже есть")
    if name_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с таким именем уже есть")

    hashed_password = auth.hash_value(password)
    user = User(full_name=full_name, email=email, password=hashed_password, permissions=Permissions.NONE)
    await user.insert()

    return {
        "status": "success"
    }

