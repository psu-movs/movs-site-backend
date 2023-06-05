from fastapi import HTTPException, status


class MissingPermissions(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You're missing permissions for this action",
        )


class InvalidUserData(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )


class DepartmentInfoDoesNotExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There are no information about department. Please, add it."
        )


class DepartmentHeadDoesNotExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="There are no information about department head. Please, add it."
        )