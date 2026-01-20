"""
app/routers/pages.py
HTML page rendering routes
"""

from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, RedirectResponse
from pathlib import Path
import os


router = APIRouter()

# Get the templates directory path
TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates"


@router.get("/")
async def landing_page(request: Request):
    """Serve landing/hero page"""
    template_path = TEMPLATES_DIR / "hero.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/login")
async def login_page(request: Request):
    """Serve login page"""
    template_path = TEMPLATES_DIR / "login.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/register")
async def register_page(request: Request):
    """Serve registration page"""
    template_path = TEMPLATES_DIR / "signup.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/verify-email")
async def verify_email_page(request: Request):
    """Serve email verification page"""
    template_path = TEMPLATES_DIR / "email_verification.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/forgot-password")
async def forgot_password_page(request: Request):
    """Serve forgot password page"""
    template_path = TEMPLATES_DIR / "forgot_password.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/reset-password")
async def reset_password_page(request: Request):
    """Serve password reset page"""
    template_path = TEMPLATES_DIR / "set_new_password.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/dashboard")
async def dashboard_page(request: Request):
    """Serve dashboard page - requires authentication in production"""
    template_path = TEMPLATES_DIR / "dashboard.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/auth/callback")
async def oauth_callback_page(request: Request):
    """Serve OAuth callback page"""
    template_path = TEMPLATES_DIR / "callback.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/results/{job_id}")
async def results_page(request: Request, job_id: str):
    """Serve OCR results page"""
    template_path = TEMPLATES_DIR / "results.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/settings")
async def settings_page(request: Request):
    """Serve settings/profile page - requires authentication in production"""
    template_path = TEMPLATES_DIR / "settings.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")


@router.get("/features")
async def features_page(request: Request):
    """Serve features page"""
    template_path = TEMPLATES_DIR / "features.html"
    if template_path.exists():
        return FileResponse(template_path, media_type="text/html")
    return RedirectResponse(url="/docs")
