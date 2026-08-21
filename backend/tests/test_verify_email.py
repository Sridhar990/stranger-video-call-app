from datetime import datetime, timedelta

from models import User, UserToken, TokenType
from utils import hash_password


def create_verification_user(
    db,
    *,
    token_type=TokenType.EMAIL_VERIFICATION,
    used=False,
    is_verified=False,
    expires_at=None,
):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=is_verified,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    if expires_at is None:
        expires_at = datetime.utcnow() + timedelta(hours=1)

    user_token = UserToken(
        user_id=user.id,
        token="verification-token",
        token_type=token_type,
        expires_at=expires_at,
        used=used,
    )

    db.add(user_token)
    db.commit()
    db.refresh(user_token)

    return user, user_token


def test_verify_email_success(client, db):
    user, user_token = create_verification_user(db)

    response = client.get(
        f"/auth/verify-email?token={user_token.token}"
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Email verified successfully"
    }

    db.refresh(user)
    db.refresh(user_token)

    assert user.is_verified is True
    assert user_token.used is True


def test_verify_email_invalid_token(client):
    response = client.get(
        "/auth/verify-email?token=invalid-token"
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid verification link"
    }


def test_verify_email_wrong_token_type(client, db):
    _, user_token = create_verification_user(
        db,
        token_type=TokenType.PASSWORD_RESET,
    )

    response = client.get(
        f"/auth/verify-email?token={user_token.token}"
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid token type"
    }


def test_verify_email_token_already_used(client, db):
    _, user_token = create_verification_user(
        db,
        used=True,
    )

    response = client.get(
        f"/auth/verify-email?token={user_token.token}"
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Verification link already used"
    }


def test_verify_email_token_expired(client, db):
    _, user_token = create_verification_user(
        db,
        expires_at=datetime.utcnow() - timedelta(hours=1),
    )

    response = client.get(
        f"/auth/verify-email?token={user_token.token}"
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Verification link expired"
    }


def test_verify_email_already_verified(client, db):
    _, user_token = create_verification_user(
        db,
        is_verified=True,
    )

    response = client.get(
        f"/auth/verify-email?token={user_token.token}"
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email already verified"
    }