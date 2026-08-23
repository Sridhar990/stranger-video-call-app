from fastapi import HTTPException, status
from models import TokenType
from repositories.user_token_repository import get_token
from datetime import datetime


def logout(refresh_token: str, db):
    token_record = get_token(
        db=db,
        token=refresh_token,
    )

    if token_record is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    if token_record.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired",
        )

    if token_record.token_type != TokenType.REFRESH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    if token_record.used:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token already revoked",
        )

    token_record.used = True
    db.commit()

    return {
        "message": "Logged out successfully"
    }