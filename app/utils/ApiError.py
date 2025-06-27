from typing import Any

from fastapi import HTTPException


class ApiError(HTTPException):
    def __init__(
        self,
        message: str = "Something went wrong",
        status_code: int = 400,
        error: list[Any] = [],
    ):
        self.error = error  # ✅ store the error list in the instance
        super().__init__(
            status_code=status_code,
            detail={
                "status": "error",
                "message": message,
                "errors": self.error,
            },  # When raising an HTTPException, you can pass any value that can be converted to JSON as the parameter detail, not only str.You could pass a dict, a list, etc.They are handled automatically by FastAPI and converted to JSON.
        )
