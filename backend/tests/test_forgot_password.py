from datetime import datetime

from models import User, UserToken, TokenType
from utils import hash_password


def test_forgot_password_success(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/forgot-password",
        json={
            "email": "sridhar@test.com",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": (
            "If an account with that email exists, "
            "a password reset link has been sent."
        )
    }

    token = (
        db.query(UserToken)
        .filter(
            UserToken.user_id == user.id,
            UserToken.token_type == TokenType.PASSWORD_RESET,
        )
        .first()
    )

    assert token is not None
    assert token.used is False
    assert token.expires_at > datetime.utcnow()


def test_forgot_password_email_not_found(client, db):
    response = client.post(
        "/auth/forgot-password",
        json={"email": "unknown@test.com"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "If an account with that email exists, a password reset link has been sent."
    }

    token = db.query(UserToken).first()
    assert token is None

def test_forgot_password_email_normalization(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/forgot-password",
        json={
            "email": "  SRIDHAR@TEST.COM  ",
        },
    )

    assert response.status_code == 200

    token = (
        db.query(UserToken)
        .filter(UserToken.user_id == user.id)
        .first()
    )

    assert token is not None

def test_forgot_password_email_not_verified(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=False,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/forgot-password",
        json={"email": "sridhar@test.com"},
    )

    assert response.status_code == 200

    token = db.query(UserToken).first()
    assert token is None


def test_forgot_password_account_disabled(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=False,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/forgot-password",
        json={"email": "sridhar@test.com"},
    )

    assert response.status_code == 200

    token = db.query(UserToken).first()
    assert token is None

def test_forgot_password_token_type(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    client.post(
        "/auth/forgot-password",
        json={"email": "sridhar@test.com"},
    )

    token = db.query(UserToken).first()

    assert token.token_type == TokenType.PASSWORD_RESET


def test_forgot_password_token_unused(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    client.post(
        "/auth/forgot-password",
        json={"email": "sridhar@test.com"},
    )

    token = db.query(UserToken).first()

    assert token.used is False


def test_forgot_password_creates_one_token(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    client.post(
        "/auth/forgot-password",
        json={"email": "sridhar@test.com"},
    )

    count = db.query(UserToken).count()

    assert count == 1