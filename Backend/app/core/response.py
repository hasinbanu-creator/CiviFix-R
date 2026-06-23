from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

class ResponseHandler:

    @staticmethod
    def success(
        message: str,
        data=None,
        status_code: int = 200
    ):
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder({
                "success": True,
                "message": message,
                "data": data
            })
        )

    @staticmethod
    def error(
        message: str,
        errors=None,
        status_code: int = 400
    ):
        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder({
                "success": False,
                "message": message,
                "errors": errors
            })
        )

class SuccessResponse:

    @staticmethod
    def create(
        message: str,
        data=None,
        status_code: int = 200
    ):
        return ResponseHandler.success(
            message=message,
            data=data,
            status_code=status_code
        )


class ErrorResponse:

    @staticmethod
    def create(
        message: str,
        errors=None,
        status_code: int = 400
    ):
        return ResponseHandler.error(
            message=message,
            errors=errors,
            status_code=status_code
        )
