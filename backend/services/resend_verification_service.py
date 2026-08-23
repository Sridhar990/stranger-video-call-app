from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from repositories.user_repository import get_user_by_email
from services.token_service import generate_user_token
from services.email_service import send_verification_email
from config import FRONTEND_URL
from models import TokenType


async def resend_verification(
    db: Session,
    email: str,
):
    user = get_user_by_email(
        db=db,
        email=email,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already verified",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    user_token = generate_user_token(
        db=db,
        user=user,
        token_type=TokenType.EMAIL_VERIFICATION,
    )

    verification_link = (
        f"{FRONTEND_URL}/verify-email?token={user_token.token}"
    )

    await send_verification_email(
        email=user.email,
        username=user.username,
        verification_link=verification_link,
    )

    return {
        "message": "Verification email sent successfully"
    }