"""Server-rendered UI routes for the local SpecForge demo."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from specforge.ui.service import (
    analyze_for_ui,
    default_demo_name,
    demo_options,
    generate_for_ui,
    load_demo_brief,
)

router = APIRouter(include_in_schema=False)
TEMPLATES = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))


@router.get("/", response_class=HTMLResponse)
@router.get("/ui", response_class=HTMLResponse)
def ui_home(request: Request, demo: str | None = None) -> HTMLResponse:
    """Render the local demo UI home page."""

    demo_name = demo or default_demo_name()
    title, brief_text = load_demo_brief(demo_name)
    return render_page(
        request=request,
        brief_text=brief_text,
        title=title,
        selected_demo=demo_name,
        output_label="",
    )


@router.post("/ui/analyze", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def ui_analyze(
    request: Request,
    brief_text: str = Form(...),
    title: str = Form(""),
    demo_name: str = Form(default_demo_name()),
) -> HTMLResponse:
    """Analyze a brief and render the result in the browser UI."""

    try:
        result = analyze_for_ui(
            brief_text=brief_text,
            title=title or None,
            source_type="ui",
        )
        error_message = None
    except (ValidationError, HTTPException) as exc:
        result = None
        error_message = render_error(exc)
    return render_page(
        request=request,
        brief_text=brief_text,
        title=title,
        selected_demo=demo_name,
        result=result,
        active_step="analysis",
        error_message=error_message,
    )


@router.post("/ui/generate", response_class=HTMLResponse, status_code=status.HTTP_200_OK)
def ui_generate(
    request: Request,
    brief_text: str = Form(...),
    title: str = Form(""),
    output_label: str = Form(""),
    demo_name: str = Form(default_demo_name()),
) -> HTMLResponse:
    """Generate a delivery bundle and render the result in the browser UI."""

    try:
        result = generate_for_ui(
            brief_text=brief_text,
            title=title or None,
            output_label=output_label or None,
        )
        error_message = None
    except (ValidationError, HTTPException) as exc:
        result = None
        error_message = render_error(exc)
    return render_page(
        request=request,
        brief_text=brief_text,
        title=title,
        output_label=output_label,
        selected_demo=demo_name,
        result=result,
        active_step="generation",
        error_message=error_message,
    )


def render_page(
    *,
    request: Request,
    brief_text: str,
    title: str,
    selected_demo: str,
    output_label: str = "",
    result: object | None = None,
    active_step: str = "intake",
    error_message: str | None = None,
) -> HTMLResponse:
    """Render the main SpecForge UI template."""

    return TEMPLATES.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "brief_text": brief_text,
            "title": title,
            "output_label": output_label,
            "selected_demo": selected_demo,
            "demo_options": demo_options(),
            "result": result,
            "active_step": active_step,
            "error_message": error_message,
        },
    )


def render_error(exc: ValidationError | HTTPException) -> str:
    """Convert validation and HTTP errors into a short UI message."""

    if isinstance(exc, HTTPException):
        return str(exc.detail)
    errors = exc.errors()
    if errors:
        return errors[0].get("msg", "Validation failed.")
    return "Validation failed."
