from sqlalchemy.orm import Session

from models import User
from repositories.user_token_repository import (
    revoke_all_refresh_tokens,
)


def logout_all_devices(
    db: Session,
    current_user: User,
):
    revoke_all_refresh_tokens(
        db=db,
        user_id=current_user.id,
    )

    return {
        "message": "Logged out from all devices successfully",
    }