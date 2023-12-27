from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY
from tortoise.exceptions import DoesNotExist

from owjcommon.exceptions import OWJException


async def owj_exception_handler(request: Request, exc: OWJException):
    return JSONResponse(
        status_code=exc.http_status_code,
        content={
            "success": False,
            "error": {"id": exc.code, "message": exc.message},
        },
    )


async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        {
            "success": False,
            "error": {"id": "E1000", "message": exc.detail},
        },
        status_code=exc.status_code,
        headers=headers,
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "id": "E1001",
                "message": "validation_error",
                "detail": jsonable_encoder(exc.errors()),
            },
        },
    )


async def tortoise_not_found_exception_handler(
    request: Request, exc: DoesNotExist
) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    return JSONResponse(
        {
            "success": False,
            "error": {"id": "E1023", "message": "Object not found in database"},
        },
        status_code=404,
        headers=headers,
    )
