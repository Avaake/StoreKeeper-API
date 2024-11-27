def test_valid_registration(test_client, init_db):
    response = test_client.post(
        "api/v1/auth/registration",
        json={
            "username": "test_user",
            "email": "test_user@gmail.com",
            "password": "test_user_password",
        },
    )

    assert response.status_code == 201
    assert "User registered successfully" in response.json["message"]
    assert "id" in response.json["user"]
    assert "username" in response.json["user"]
    assert "email" in response.json["user"]
    assert "password" not in response.json["user"]


def test_invalid_registration(test_client, init_db):
    response = test_client.post(
        "api/v1/auth/registration",
        json={
            "username": "test_user1",
            "email": "test_user1@gmail.com",
            "password": "te",
        },
    )

    assert response.status_code == 422
    assert "password" not in response.json["error"]
    assert response.json["error"] == "Validation error"


def test_duplicate_registration(test_client, init_db):
    # Перший запит для реєстрації користувача
    response = test_client.post(
        "api/v1/auth/registration",
        json={
            "username": "test_user_duplicate",
            "email": "test_user_duplicate@gmail.com",
            "password": "test_user_duplicate",
        },
    )

    assert response.status_code == 201

    response_duplicate = test_client.post(
        "api/v1/auth/registration",
        json={
            "username": "test_user_duplicate1",
            "email": "test_user_duplicate@gmail.com",
            "password": "test_user_duplicate1",
        },
    )

    assert response_duplicate.status_code == 400
    assert response_duplicate.json["error"] == "A user with this email already exists!"


def test_valid_login(test_client, init_db):
    response = test_client.post(
        "api/v1/auth/login",
        json={
            "email": "sem@gmail.com",
            "password": "sem_password",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_invalid_login(test_client, init_db):
    response_first = test_client.post(
        "api/v1/auth/login",
        json={
            "email": "se@gmail.com",
            "password": "sem_password",
        },
    )

    assert response_first.status_code == 422
    assert "Incorrect email or password!" in response_first.json["error"]

    response_second = test_client.post(
        "api/v1/auth/login",
        json={
            "email": "sem@gmail.com",
            "password": "password",
        },
    )

    assert response_second.status_code == 422
    assert "Incorrect email or password!" in response_second.json["error"]


def test_refresh_token(test_client, init_db, sem_token):
    response = test_client.post(
        "api/v1/auth/refresh",
        headers={
            "Authorization": f"Bearer {sem_token[-1]}",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json


def test_full_session(test_client, init_db):
    response_reg = test_client.post(
        "api/v1/auth/registration",
        json={
            "username": "john_test",
            "email": "john_test@gmail.com",
            "password": "john_test",
        },
    )

    assert response_reg.status_code == 201
    assert "password" not in response_reg.json["user"]

    response_login = test_client.post(
        "api/v1/auth/login",
        json={
            "email": "john_test@gmail.com",
            "password": "john_test",
        },
    )
    assert response_login.status_code == 200
    assert "access_token" in response_login.json
    assert "refresh_token" in response_login.json

    refresh_token = response_login.json["refresh_token"]

    response_refresh = test_client.post(
        "api/v1/auth/refresh",
        headers={
            "Authorization": f"Bearer {refresh_token}",
        },
    )

    assert response_refresh.status_code == 200
    assert "access_token" in response_refresh.json
