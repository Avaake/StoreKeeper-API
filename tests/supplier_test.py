def test_create_supplier(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/suppliers",
        json={
            "name": "test_supplier",
            "email": "test_supplier@example.com",
            "phone_number": "0970390384",
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 201
    assert "supplier" in response.json
    assert "name" in response.json["supplier"]
    assert response.json["supplier"]["address"] is None


def test_create_supplier_validate_error(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/suppliers",
        json={
            "name": "test_supplier2",
            "email": "test_supplier2@example.com",
            "phone_number": "0970390",
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 422
    assert "error" in response.json
    assert response.json["error"] == "Validation error"
    assert response.json["details"] != {}


def test_get_all_suppliers(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/suppliers",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert response.json["suppliers"] != []
    assert isinstance(response.json["suppliers"], list)


def test_get_supplier(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/suppliers/2",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["supplier"]["name"] == "test_supplier"
    assert response.json["supplier"]["email"] == "test_supplier@example.com"
    assert response.json["supplier"]["phone_number"] == "0970390384"
    assert response.json["supplier"]["address"] is None


def test_search_supplier_with_name(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/suppliers/search?q=t_supp",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["suppliers"] != []
    assert response.json["suppliers"][0]["name"] == "test_supplier"


def test_update_supplier(test_client, init_db, sem_token):
    response = test_client.patch(
        "/api/v1/suppliers/2",
        json={"address": "Test Address"},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert response.json["supplier"]["address"] == "Test Address"


def test_delete_supplier(test_client, init_db, sem_token):
    response = test_client.delete(
        "/api/v1/suppliers/2",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 204
