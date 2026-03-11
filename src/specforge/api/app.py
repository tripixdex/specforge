"""Application factory and top-level FastAPI app for SpecForge."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from specforge.api.routes import router
from specforge.api.schemas import ErrorResponse
from specforge.ui.routes import router as ui_router


def create_app() -> FastAPI:
    """Create the SpecForge local demo API application."""

    app = FastAPI(
        title="SpecForge Local Demo",
        version="0.6.0",
        summary=(
            "Typed local API, browser UI, and evaluation harness for the deterministic "
            "SpecForge pipeline."
        ),
    )
    app.include_router(router)
    app.include_router(ui_router)
    static_dir = Path(__file__).resolve().parents[1] / "ui" / "static"
    app.mount("/ui-static", StaticFiles(directory=str(static_dir)), name="ui-static")

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        """Return normalized validation responses without stack traces."""

        del request
        payload = ErrorResponse(
            error="validation_error",
            detail=jsonable_encoder(exc.errors()),
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=payload.model_dump(),
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Return a generic error body for unexpected failures."""

        del request, exc
        payload = ErrorResponse(
            error="internal_error",
            detail="SpecForge hit an unexpected local error while handling the request.",
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=payload.model_dump(),
        )

    return app


app = create_app()
