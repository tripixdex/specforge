"""Route definitions for the SpecForge FastAPI app."""

from __future__ import annotations

from fastapi import APIRouter, status

from specforge.api.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    DemoResponse,
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
)
from specforge.api.service import (
    analyze_request,
    build_analyze_response,
    build_demo_response,
    generate_response,
)

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health() -> HealthResponse:
    """Report local API health."""

    return HealthResponse()


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    status_code=status.HTTP_200_OK,
    tags=["analysis"],
)
def analyze(payload: AnalyzeRequest) -> AnalyzeResponse:
    """Run deterministic analysis without writing files."""

    brief, report = analyze_request(payload)
    return build_analyze_response(brief, report)


@router.post(
    "/generate",
    response_model=GenerateResponse,
    status_code=status.HTTP_200_OK,
    tags=["generation"],
)
def generate(payload: GenerateRequest) -> GenerateResponse:
    """Run the deterministic pipeline and export a repo-local bundle."""

    return generate_response(payload)


@router.get("/demo", response_model=DemoResponse, tags=["demo"])
def demo() -> DemoResponse:
    """Return a stable demo response based on a bundled sample brief."""

    return build_demo_response()
