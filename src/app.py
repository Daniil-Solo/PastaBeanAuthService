from fastapi import FastAPI, Request
from fastapi import status
from fastapi.responses import JSONResponse
from src.config import app_config
from src.endpoints.routers.auth import router as auth_router
from src.endpoints.routers.user import router as user_router
from src.endpoints.exceptions import ApplicationException
from src.services.exceptions import ServiceException, NeedAuthException, SuchUserDoesntExistException


def add_service_exceptions(application: FastAPI) -> None:
    @application.exception_handler(ServiceException)
    async def unicorn_exception_handler(_: Request, exc: ServiceException):
        status_code = status.HTTP_400_BAD_REQUEST
        if isinstance(exc, NeedAuthException):
            status_code = status.HTTP_401_UNAUTHORIZED
        elif isinstance(exc, SuchUserDoesntExistException):
            status_code = status.HTTP_404_NOT_FOUND
        return JSONResponse(
            status_code=status_code,
            content={"message": exc.message},
        )


def add_other_exceptions(application: FastAPI) -> None:
    @application.exception_handler(ApplicationException)
    async def unicorn_exception_handler(_: Request, exc: ApplicationException):
        return JSONResponse(
            status_code=exc.status,
            content={"message": exc.message},
        )


def add_routers(application: FastAPI) -> None:
    application.include_router(auth_router)
    application.include_router(user_router)


def create_application() -> FastAPI:
    application = FastAPI(
        title="Shop Placement Platform",
        version="0.0.1",
        docs_url="/docs" if app_config.is_debug else None,
        redoc_url="/docs/redoc" if app_config.is_debug else None,
    )
    add_service_exceptions(application)
    add_other_exceptions(application)
    add_routers(application)
    return application


app = create_application()
