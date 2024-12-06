def test_create_category(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/categories",
        json={"name": "pixel"},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 201
    assert "id" in response.json["category"]
    assert "name" in response.json["category"]


def test_get_categories(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    for category in response.json["categories"]:
        assert "id" in category
        assert "name" in category


def test_get_category_by_id(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/categories/1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert "id" in response.json["category"]


def test_update_category(test_client, init_db, sem_token):
    response = test_client.patch(
        "/api/v1/categories/2",
        json={"name": "poco"},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert "poco" in response.json["category"]["name"]


def test_invalid_update_category(test_client, init_db, sem_token):
    response_not_found_id = test_client.patch(
        "/api/v1/categories/10",
        json={"name": "pixel"},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response_not_found_id.status_code == 404
    assert response_not_found_id.json["error"] == "404 Not Found: Category not found"

    response_valid_error = test_client.patch(
        "/api/v1/categories/1",
        json={"name": 123},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response_valid_error.status_code == 422
    assert response_valid_error.json["error"] == "Validation error"


def test_delete_category(test_client, init_db, sem_token):
    response = test_client.delete(
        "/api/v1/categories/1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 204


def test_full_category(test_client, init_db, sem_token):
    response_create = test_client.post(
        "/api/v1/categories",
        json={"name": "huawei"},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response_create.status_code == 201
    assert "name" in response_create.json["category"]

    category_id = response_create.json["category"]["id"]

    response_get = test_client.get(
        f"/api/v1/categories/{category_id}",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response_get.status_code == 200
    assert response_get.json["category"]["id"] == category_id

    response_update = test_client.patch(
        f"/api/v1/categories/{category_id}",
        json={"name": "xiaomi"},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response_update.status_code == 200
    assert response_update.json["category"]["name"] == "xiaomi"

    response_delete = test_client.delete(
        f"/api/v1/categories/{category_id}",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response_delete.status_code == 204
