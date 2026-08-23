from fastapi import HTTPException, status

from datetime import datetime

from sqlalchemy.orm import Session

from schemas.user import ResetPasswordRequest

from models import TokenType

from repositories.user_repository import (
    get_user_by_id,
    update_password,
)

from repositories.user_token_repository import (
    get_token,
    mark_token_as_used,
)

from utils import hash_password


def reset_password(
    request: ResetPasswordRequest,
    db: Session,
):
    user_token = get_token(
        db=db,
        token=request.token,
    )

    if user_token is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token",
        )

    if user_token.token_type != TokenType.PASSWORD_RESET:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token",
        )

    if user_token.used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token already used",
        )

    if user_token.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reset token has expired",
        )

    user = get_user_by_id(
        db=db,
        user_id=user_token.user_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account has been disabled",
        )

    hashed_password = hash_password(
        request.new_password
    )

    update_password(
        db=db,
        user=user,
        hashed_password=hashed_password,
    )

    mark_token_as_used(
        db=db,
        user_token=user_token,
    )

    return {
        "message": "Password reset successfully"
    }