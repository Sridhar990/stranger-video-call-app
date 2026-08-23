from datetime import datetime, timedelta
import uuid

from models import User, UserToken, TokenType
from utils import hash_password, verify_password


def test_reset_password_success(client, db):
    old_password = hash_password("Password@123")

    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=old_password,
        is_verified=True,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = UserToken(
        user_id=user.id,
        token="reset-token",
        token_type=TokenType.PASSWORD_RESET,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
    )
    db.add(token)
    db.commit()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": "reset-token",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Password reset successfully"
    }

    db.refresh(user)
    db.refresh(token)

    assert verify_password(
        "NewPassword@123",
        user.password,
    )

    assert user.password != old_password
    assert token.used is True


def test_reset_password_invalid_token(client):
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid-token",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid reset token"
    }


def test_reset_password_wrong_token_type(client, db):
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

    token = UserToken(
        user_id=user.id,
        token="email-token",
        token_type=TokenType.EMAIL_VERIFICATION,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
    )
    db.add(token)
    db.commit()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": "email-token",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid reset token"
    }


def test_reset_password_token_already_used(client, db):
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

    token = UserToken(
        user_id=user.id,
        token="used-token",
        token_type=TokenType.PASSWORD_RESET,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
        used=True,
    )
    db.add(token)
    db.commit()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": "used-token",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Reset token already used"
    }


def test_reset_password_token_expired(client, db):
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

    token = UserToken(
        user_id=user.id,
        token="expired-token",
        token_type=TokenType.PASSWORD_RESET,
        expires_at=datetime.utcnow() - timedelta(hours=1),
    )
    db.add(token)
    db.commit()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": "expired-token",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Reset token has expired"
    }




def test_reset_password_email_not_verified(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=False,
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = UserToken(
        user_id=user.id,
        token="verify-token",
        token_type=TokenType.PASSWORD_RESET,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
    )
    db.add(token)
    db.commit()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": "verify-token",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Please verify your email"
    }


def test_reset_password_account_disabled(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = UserToken(
        user_id=user.id,
        token="disabled-token",
        token_type=TokenType.PASSWORD_RESET,
        expires_at=datetime.utcnow() + timedelta(minutes=30),
    )
    db.add(token)
    db.commit()

    response = client.post(
        "/auth/reset-password",
        json={
            "token": "disabled-token",
            "new_password": "NewPassword@123",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Your account has been disabled"
    }