from fastapi import HTTPException, status


class MissingPermissions(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="У вас недостаточно прав на выполнение этого действия!",
        )


class InvalidUserData(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неправильное имя пользователя или пароль",
        )


class DepartmentInfoDoesNotExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Нет информации о кафедре"
        )


class DepartmentInfoAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Информация о кафедре уже есть. Вы можете только обновить её",
        )


class DepartmentHeadDoesNotExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нет информации о заведующем кафедры",
        )


class DepartmentHeadAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Информации о заведующем кафедры уже есть. Вы можете только обновить её",
        )
