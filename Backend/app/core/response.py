from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.core.context import request_context
import copy

def _enrich_image_urls(data, base_url: str):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == "image_urls" and isinstance(v, list):
                # Handle old ones with /uploads and new ones without
                new_urls = []
                for url in v:
                    if str(url).startswith("http"):
                        new_urls.append(url)
                    elif str(url).startswith("/uploads/"):
                        new_urls.append(f"{base_url.rstrip('/')}{url}")
                    else:
                        new_urls.append(f"{base_url.rstrip('/')}/uploads/{url}")
                data[k] = new_urls
            else:
                _enrich_image_urls(v, base_url)
    elif isinstance(data, list):
        for item in data:
            _enrich_image_urls(item, base_url)
    return data

class ResponseHandler:

    @staticmethod
    def success(
        message: str,
        data=None,
        status_code: int = 200
    ):
        encoded_data = jsonable_encoder(data)

        # Dynamically append base URL to image_urls
        req = request_context.get()
        if req and encoded_data:
            base_url = str(req.base_url)
            encoded_data = _enrich_image_urls(encoded_data, base_url)

        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": encoded_data
            }
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
