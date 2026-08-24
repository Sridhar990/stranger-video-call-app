from datetime import datetime, timedelta

from models import User, UserToken, TokenType
from services.jwt_service import create_access_token, create_refresh_token
from repositories.user_token_repository import create_user_token
from utils import hash_password
from config import REFRESH_TOKEN_EXPIRE_DAYS

def test_logout_all_devices_success(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    for _ in range(3):
        refresh_token = create_refresh_token(str(user.id))

        create_user_token(
            db=db,
            user_token=UserToken(
                user_id=user.id,
                token=refresh_token,
                token_type=TokenType.REFRESH_TOKEN,
                expires_at=datetime.utcnow()
                + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
            ),
        )

    access_token = create_access_token(str(user.id))

    response = client.post(
        "/auth/logout-all-devices",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Logged out from all devices successfully"
    }

    tokens = db.query(UserToken).filter(
        UserToken.user_id == user.id
    ).all()

    assert len(tokens) == 3

    assert all(token.used for token in tokens)


def test_logout_all_devices_no_tokens(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(str(user.id))

    response = client.post(
        "/auth/logout-all-devices",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "Logged out from all devices successfully"
    }


def test_logout_all_devices_missing_token(client):
    response = client.post("/auth/logout-all-devices")

    assert response.status_code == 401


def test_logout_all_devices_invalid_token(client):
    response = client.post(
        "/auth/logout-all-devices",
        headers={
            "Authorization": "Bearer invalid.jwt.token",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid or expired token",
    }


def test_logout_all_devices_user_not_found(client):
    access_token = create_access_token(
        user_id="11111111-1111-1111-1111-111111111111"
    )

    response = client.post(
        "/auth/logout-all-devices",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "User not found",
    }


