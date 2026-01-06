"""
app/routers/pages.py
HTML page rendering routes
"""

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.core.dependencies import get_optional_user


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def landing_page(
    request: Request,
    user = Depends(get_optional_user)
):
    """Landing page"""
    return templates.TemplateResponse(
        "landing.html",
        {"request": request, "user": user}
    )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page"""
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request}
    )


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Registration page"""
    return templates.TemplateResponse(
        "auth/register.html",
        {"request": request}
    )


@router.get("/verify-email", response_class=HTMLResponse)
async def verify_email_page(request: Request):
    """Email verification page"""
    return templates.TemplateResponse(
        "auth/verify_email.html",
        {"request": request}
    )


@router.get("/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Forgot password page"""
    return templates.TemplateResponse(
        "auth/forgot_password.html",
        {"request": request}
    )


@router.get("/reset-password", response_class=HTMLResponse)
async def reset_password_page(request: Request):
    """Reset password page"""
    return templates.TemplateResponse(
        "auth/reset_password.html",
        {"request": request}
    )


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
    request: Request,
    user = Depends(get_optional_user)
):
    """Dashboard/upload page"""
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Please login to access dashboard"}
        )
    
    return templates.TemplateResponse(
        "app/dashboard.html",
        {"request": request, "user": user}
    )


@router.get("/results/{job_id}", response_class=HTMLResponse)
async def results_page(
    request: Request,
    job_id: str,
    user = Depends(get_optional_user)
):
    """OCR results page"""
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Please login to view results"}
        )
    
    return templates.TemplateResponse(
        "app/results.html",
        {"request": request, "user": user, "job_id": job_id}
    )


@router.get("/settings", response_class=HTMLResponse)
async def settings_page(
    request: Request,
    user = Depends(get_optional_user)
):
    """Account settings page"""
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Please login to access settings"}
        )
    
    return templates.TemplateResponse(
        "app/settings.html",
        {"request": request, "user": user}
    )
