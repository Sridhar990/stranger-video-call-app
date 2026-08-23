from models import User


def test_resend_verification_success(client, db):
    # Create an unverified user
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password="hashedpassword",
        is_verified=False,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Call endpoint
    response = client.post(
        "/auth/resend-verification",
        json={
            "email": "sridhar@test.com",
        },
    )

    # Assertions
    assert response.status_code == 200
    assert response.json() == {
        "message": "Verification email sent successfully"
    }

def test_resend_verification_user_not_found(client):
    response = client.post(
        "/auth/resend-verification",
        json={
            "email": "notfound@test.com",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "User not found"
    }


from models import User


def test_resend_verification_already_verified(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password="hashedpassword",
        is_verified=True,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post(
        "/auth/resend-verification",
        json={
            "email": "sridhar@test.com",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Email is already verified"
    }

from models import User


def test_resend_verification_account_disabled(client, db):
    user = User(
        username="sridhar90",
        email="sridhar@test.com",
        password="hashedpassword",
        is_verified=False,
        is_active=False,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    response = client.post(
        "/auth/resend-verification",
        json={
            "email": "sridhar@test.com",
        },
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "Account is disabled"
    }