from fastapi import APIRouter,status,Depends,Query
from schemas.user import UserCreate,LoginRequest,RefreshTokenRequest,ResetPasswordRequest,ForgotPasswordRequest,ResendVerificationRequest
from sqlalchemy.orm import Session
from services.email_service import send_verification_email
from services.auth_service import register_user
from dependencies import get_db
from services.email_verification_service import verify_email
from services.login_service import login_user
from fastapi.security import OAuth2PasswordRequestForm
from services.auth_refresh_service import refresh_access_token
from services.forgot_password_service import forgot_password
from services.reset_password_service import reset_password
from services.resend_verification_service import (
    resend_verification,
)





router = APIRouter(prefix= "/auth",tags=["Authentication"])

@router.get("/test")
def test():
    return {
        "message": "Authetication is working"
    }

@router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate,db:Session = Depends(get_db)):
    return await register_user(user,db)


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
async def login(
    user: LoginRequest,
    db: Session = Depends(get_db),
):
    return await login_user(
        user=user,
        db=db,
    )

@router.post("/token")
async def oauth_login(
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
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token(
        refresh_token=request.refresh_token,
        db=db,
    )


@router.post("/forgot-password")
async def forgot_password_route(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    return await forgot_password(
        request=request,
        db=db,
    )


@router.post("/reset-password")
def reset_password_route(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    return reset_password(
        request=request,
        db=db,
    )


@router.post("/resend-verification")
async def resend_verification_route(
    request: ResendVerificationRequest,
    db: Session = Depends(get_db),
):
    return await resend_verification(
        db=db,
        email=request.email,
    )