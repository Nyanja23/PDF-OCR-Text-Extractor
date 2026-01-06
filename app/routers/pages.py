"""
app/routers/pages.py
HTML page rendering routes
"""

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, JSONResponse


router = APIRouter()


@router.get("/")
async def landing_page(request: Request):
    """API-only backend: redirect to Swagger UI"""
    return RedirectResponse(url="/docs")


@router.get("/login")
async def login_page(request: Request):
    return RedirectResponse(url="/docs")


@router.get("/register")
async def register_page(request: Request):
    return RedirectResponse(url="/docs")


@router.get("/verify-email")
async def verify_email_page(request: Request):
    return RedirectResponse(url="/docs")


@router.get("/forgot-password")
async def forgot_password_page(request: Request):
    return RedirectResponse(url="/docs")


@router.get("/reset-password")
async def reset_password_page(request: Request):
    return RedirectResponse(url="/docs")


@router.get("/dashboard")
async def dashboard_page(request: Request):
    return RedirectResponse(url="/docs")


@router.get("/results/{job_id}")
async def results_page(request: Request, job_id: str):
    return JSONResponse({"detail": "Use /api/ocr or /api/users endpoints; see /docs"})


@router.get("/settings")
async def settings_page(request: Request):
    return RedirectResponse(url="/docs")
