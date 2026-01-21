"""
app/routers/auth.py
Authentication API endpoints
"""

from fastapi import APIRouter, Depends, Response, Request, HTTPException
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.schemas.auth import (
    OTPVerify, PasswordResetRequest, PasswordReset, TokenResponse
)
from app.services.auth_service import AuthService
from app.core.config import settings


router = APIRouter()

# OAuth configuration
oauth = OAuth()
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)


@router.post("/register", response_model=dict)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user"""
    try:
        auth_service = AuthService(db)
        user, otp_code = auth_service.register_user(user_data)

        return {
            "message": "Registration successful. Please check your email for verification code.",
            "email": user.email,
            "user_id": user.id
        }
    except HTTPException:
        # Let FastAPI handle known HTTPExceptions
        raise
    except Exception as e:
        # Log full traceback to console for debugging, then return 500
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.post("/verify-email", response_model=dict)
async def verify_email(
    verify_data: OTPVerify,
    response: Response,
    db: Session = Depends(get_db)
):
    """Verify user email with OTP"""
    auth_service = AuthService(db)
    user = auth_service.verify_email(verify_data.email, verify_data.code)
    
    return {
        "message": "Email verified successfully. You can now login.",
        "user_id": user.id
    }


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Login user"""
    try:
        auth_service = AuthService(db)
        
        # Get client info
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        # Authenticate user
        user, session_id = auth_service.login(
            login_data.email,
            login_data.password,
            ip_address,
            user_agent
        )
        
        # Set session cookie
        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=not settings.DEBUG,  # HTTPS only in production
            samesite="lax",
            max_age=settings.SESSION_DURATION_DAYS * 24 * 60 * 60
        )
        
        return TokenResponse(
            access_token=session_id,
            user=UserResponse.from_orm(user)
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print("\n[LOGIN ERROR] Exception occurred:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/logout")
async def logout(
    response: Response,
    session_id: str = None,
    db: Session = Depends(get_db)
):
    """Logout user"""
    if session_id:
        auth_service = AuthService(db)
        auth_service.logout(session_id)
    
    # Clear session cookie
    response.delete_cookie(key="session_id")
    
    return {"message": "Logged out successfully"}


@router.post("/password-reset/request", response_model=dict)
async def request_password_reset(
    reset_request: PasswordResetRequest,
    db: Session = Depends(get_db)
):
    """Request password reset"""
    auth_service = AuthService(db)
    message = auth_service.request_password_reset(reset_request.email)
    
    return {"message": message}


@router.post("/password-reset/confirm", response_model=dict)
async def reset_password(
    reset_data: PasswordReset,
    db: Session = Depends(get_db)
):
    """Reset password with OTP"""
    auth_service = AuthService(db)
    user = auth_service.reset_password(
        reset_data.email,
        reset_data.code,
        reset_data.new_password
    )
    
    return {
        "message": "Password reset successfully. Please login with your new password."
    }


@router.get("/google")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """Google OAuth callback"""
    try:
        # Get token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info
        user_info = token.get('userinfo')
        if not user_info:
            return RedirectResponse(url="/auth/callback?error=user_info_not_found&error_description=Failed%20to%20get%20user%20info")
        
        email = user_info.get('email')
        name = user_info.get('name', '')
        
        if not email:
            return RedirectResponse(url="/auth/callback?error=no_email&error_description=Email%20not%20provided%20by%20Google")
        
        # Create or get user
        auth_service = AuthService(db)
        user = auth_service.create_oauth_user(email, name, "google")
        
        # Create session
        ip_address = request.client.host
        user_agent = request.headers.get("user-agent", "")
        _, session_id = auth_service.login(email, None, ip_address, user_agent)
        
        # Redirect to callback page with authorization code
        # The callback.html page will handle the redirect to dashboard
        callback_response = RedirectResponse(url="/auth/callback?code=oauth_success")
        callback_response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=not settings.DEBUG,
            samesite="lax",
            max_age=settings.SESSION_DURATION_DAYS * 24 * 60 * 60
        )
        
        return callback_response
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        error_msg = str(e).replace(" ", "%20")
        return RedirectResponse(url=f"/auth/callback?error=oauth_failed&error_description={error_msg}")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """Get current user information"""
    return UserResponse.from_orm(current_user)