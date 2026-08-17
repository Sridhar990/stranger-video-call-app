def test_register_success(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 201

def test_register_duplicate_email(client):
    # Register first user
    client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    # Try to register another user with the same email
    response = client.post(
        "/auth/register",
        json={
            "username": "anotheruser",
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 400


def test_register_duplicate_username(client):
    # Register first user
    client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    # Try to register another user with the same username
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "another@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 400

def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "not-an-email",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422


def test_register_missing_username(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422

def test_register_missing_password(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "sridhar@test.com",
        },
    )

    assert response.status_code == 422


def test_register_missing_email(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422

# username validate checking

def test_register_username_too_short(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "srid",   # 4 characters
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422

def test_register_username_too_long(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "a" * 31,
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422

def test_register_username_invalid_characters(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar@90",
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422

def test_register_username_contains_spaces(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar 90",
            "email": "sridhar@test.com",
            "password": "Password@123",
        },
    )

    assert response.status_code == 422

 # password validation check

def test_register_password_too_short(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "short@test.com",
            "password": "Pass1@",  # Less than 8 characters
        },
    )

    assert response.status_code == 422


def test_register_password_too_long(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "long@test.com",
            "password": "A" * 129,
        },
    )

    assert response.status_code == 422

def test_register_password_missing_uppercase(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "upper@test.com",
            "password": "password@123",
        },
    )

    assert response.status_code == 422

def test_register_password_missing_lowercase(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "lower@test.com",
            "password": "PASSWORD@123",
        },
    )

    assert response.status_code == 422

def test_register_password_missing_number(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "number@test.com",
            "password": "Password@",
        },
    )

    assert response.status_code == 422

def test_register_password_missing_special_character(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "special@test.com",
            "password": "Password123",
        },
    )

    assert response.status_code == 422

def test_register_password_contains_spaces(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "sridhar90",
            "email": "space@test.com",
            "password": "Password @123",
        },
    )

    assert response.status_code == 422








