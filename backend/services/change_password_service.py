from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import User
from schemas.user import ChangePasswordRequest
from utils import verify_password, hash_password


def change_password(
    request: ChangePasswordRequest,
    current_user: User,
    db: Session,
):
    if not verify_password(
        request.current_password,
        current_user.password,
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )

    if request.current_password == request.new_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from current password",
        )

    current_user.password = hash_password(
        request.new_password,
    )

    db.commit()

    return {
        "message": "Password changed successfully",
    }