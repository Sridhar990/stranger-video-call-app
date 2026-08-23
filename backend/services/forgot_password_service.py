from sqlalchemy.orm import Session

from config import FRONTEND_URL
from models import TokenType
from repositories.user_repository import get_user_by_email
from schemas.user import ForgotPasswordRequest
from services.email_service import send_password_reset_email
from services.token_service import generate_user_token


async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session,
):
    # Normalize email
    email = request.email.lower().strip()

    # Find user
    user = get_user_by_email(
        db=db,
        email=email,
    )

    # Prevent email enumeration
    if (
        user is None
        or not user.is_verified
        or not user.is_active
    ):
        return {
            "message": (
                "If an account with that email exists, "
                "a password reset link has been sent."
            )
        }

    # Generate password reset token
    user_token = generate_user_token(
        db=db,
        user=user,
        token_type=TokenType.PASSWORD_RESET,
    )

    # Build reset link
    reset_link = (
        f"{FRONTEND_URL}/reset-password?token={user_token.token}"
    )

    # Send reset email
    await send_password_reset_email(
        email=user.email,
        username=user.username,
        reset_link=reset_link,
    )

    return {
        "message": (
            "If an account with that email exists, "
            "a password reset link has been sent."
        )
    }