from models import User
from utils import hash_password


def test_oauth_login_success(client, db):
    user = User(
        username="sridhar",
        email="sridhar@test.com",
        password=hash_password("Password@123"),
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()

    response = client.post(
        "/auth/token",
        data={
            "username": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "Bearer"


def test_oauth_login_invalid_credentials(client):
    response = client.post(
        "/auth/token",
        data={
            "username": "unknown@test.com",
            "password": "WrongPassword",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Invalid email or password",
    }