
from fastapi import APIRouter, status, Depends, Query, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core.rate_limit import limiter

from schemas.user import (
    UserCreate,
    LoginRequest,
    RefreshTokenRequest,
    ResetPasswordRequest,
    ForgotPasswordRequest,
    ResendVerificationRequest,
    LogoutRequest,
    ChangePasswordRequest,
)

from dependencies import get_db, get_current_user
from models import User

from services.auth_service import register_user
from services.email_verification_service import verify_email
from services.login_service import login_user
from services.auth_refresh_service import refresh_access_token
from services.forgot_password_service import forgot_password
from services.reset_password_service import reset_password
from services.resend_verification_service import resend_verification
from services.logout_service import logout
from services.change_password_service import change_password
from services.logout_all_devices_service import logout_all_devices


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.get("/test")
def test():
    return {
        "message": "Authentication is working"
    }


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return await register_user(user, db)


@router.get("/verify-email")
def verify_email_route(
    token: str = Query(...),
    db: Session = Depends(get_db),
):
    return verify_email(
        db=db,
        token=token,
    )


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def login(
    request: Request,
    user: LoginRequest,
    db: Session = Depends(get_db),
):
    return await login_user(
        user=user,
        db=db,
    )


@router.post("/token")
@limiter.limit("5/minute")
async def oauth_login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    login_data = LoginRequest(
        email=form_data.username,
        password=form_data.password,
    )

    return await login_user(
        user=login_data,
        db=db,
    )


@router.post("/refresh")
@limiter.limit("10/minute")
def refresh_token(
    request: Request,
    request_body: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token(
        refresh_token=request_body.refresh_token,
        db=db,
    )


@router.post("/forgot-password")
@limiter.limit("3/minute")
async def forgot_password_route(
    request: Request,
    request_body: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    return await forgot_password(
        request=request_body,
        db=db,
    )


@router.post("/reset-password")
@limiter.limit("5/minute")
def reset_password_route(
    request: Request,
    request_body: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    return reset_password(
        request=request_body,
        db=db,
    )


@router.post("/resend-verification")
@limiter.limit("3/minute")
async def resend_verification_route(
    request: Request,
    request_body: ResendVerificationRequest,
    db: Session = Depends(get_db),
):
    return await resend_verification(
        db=db,
        email=request_body.email,
    )


@router.post("/logout")
@limiter.limit("10/minute")
def logout_route(
    request: Request,
    request_body: LogoutRequest,
    db: Session = Depends(get_db),
):
    return logout(
        refresh_token=request_body.refresh_token,
        db=db,
    )


@router.post("/change-password")
@limiter.limit("5/minute")
def change_password_route(
    request: Request,
    request_body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return change_password(
        request=request_body,
        current_user=current_user,
        db=db,
    )


@router.post("/logout-all-devices")
@limiter.limit("3/minute")
def logout_all_devices_route(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return logout_all_devices(
        db=db,
        current_user=current_user,
    )