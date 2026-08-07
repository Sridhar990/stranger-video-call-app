from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import TokenType
from repositories.user_token_repository import (
    get_token,
    mark_token_as_used
)
from repositories.user_repository import verify_user


def verify_email(
    db: Session,
    token: str,
):
    # Find token
    user_token = get_token(
        db=db,
        token=token,
    )

    # Token not found
    if not user_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification link",
        )

    # Wrong token type
    if user_token.token_type != TokenType.EMAIL_VERIFICATION:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid token type",
        )

    # Token already used
    if user_token.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification link already used",
        )

    # Token expired
    if user_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification link expired",
        )

    # User already verified
    if user_token.user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified",
        )

    # Verify user
    verify_user(
        db=db,
        user=user_token.user,
    )

    # Mark token as used
    mark_token_as_used(
        db=db,
        user_token=user_token,
    )

    return {
        "message": "Email verified successfully"
    }