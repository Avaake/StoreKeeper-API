def test_valid_create_user(test_client, init_db, admin_token):
    response = test_client.post(
        "api/v1/users",
        json={
            "username": "john",
            "email": "john@gmail.com",
            "password": "john_password",
            "role": "manager",
        },
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response.status_code == 201
    assert response.json["user"]["email"] == "john@gmail.com"
    assert "password" not in response.json["user"]


def test_invalid_create_user(test_client, init_db, admin_token):
    response = test_client.post(
        "api/v1/users",
        json={
            "username": "john",
            "email": "john@gmail.com",
            "password": "john_password",
            "role": "manager",
        },
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )

    assert response.status_code == 400
    assert response.json["error"] == "A user with this email already exists!"

    response = test_client.post(
        "api/v1/users",
        json={
            "username": "john",
            "email": "johngmail.com",
            "role": "manager",
        },
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response.status_code == 422
    assert response.json["error"] == "Validation error"


def test_rights_check(test_client, init_db, sem_token):
    response = test_client.post(
        "api/v1/users",
        json={
            "username": "john2",
            "email": "john2@gmail.com",
            "password": "john_password",
            "role": "manager",
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 403
    assert response.json["error"] == "Forbidden"
    assert (
        response.json["message"] == "You do not have permission to perform this action."
    )


def test_get_all_users(test_client, init_db, admin_token):
    response = test_client.get(
        "api/v1/users",
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json["users"], list)
    assert len(response.json["users"][0]) != 0


def test_get_a_user_by_id_with_admin_rights(test_client, init_db, admin_token):
    response = test_client.get(
        "api/v1/users/2",
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["user"]["email"] == "sem@gmail.com"
    assert response.json["user"]["id"] == 2


def test_get_a_user_by_id_with_user_rights(test_client, init_db, sem_token):
    response = test_client.get(
        "api/v1/users/2",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["user"]["id"] == 2

    response = test_client.get(
        "api/v1/users/1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 403
    assert response.json["error"] == "Forbidden"
    assert (
        response.json["message"] == "Access forbidden: you can only view your own data."
    )


def test_update_user(test_client, init_db, admin_token):
    response = test_client.patch(
        "api/v1/users/2",
        json={
            "email": "sem_admin@gmail.com",
            "role": "admin",
        },
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["user"]["email"] == "sem_admin@gmail.com"
    assert response.json["user"]["role"] == "admin"
    assert "password" not in response.json["user"]


def test_delete_user(test_client, init_db, admin_token):
    response = test_client.delete(
        "api/v1/users/3",
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response.status_code == 204


def test_full_users(test_client, init_db, admin_token):
    response_create = test_client.post(
        "api/v1/users",
        json={
            "username": "john3",
            "email": "john3@gmail.com",
            "password": "john3_password",
            "role": "manager",
        },
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )

    user_id = response_create.json["user"]["id"]
    assert response_create.status_code == 201

    response_get_user_by_id = test_client.get(
        f"api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response_get_user_by_id.status_code == 200

    response_update = test_client.patch(
        f"api/v1/users/{user_id}",
        json={
            "role": "smm",
        },
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response_update.status_code == 200
    assert response_update.json["user"]["role"] == "smm"

    response_delete = test_client.delete(
        f"api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token[0]}"},
    )
    assert response_delete.status_code == 204
