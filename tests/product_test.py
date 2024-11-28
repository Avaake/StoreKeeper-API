from unittest.mock import patch


def test_create_product(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/products",
        json={
            "name": "samsung 21s",
            "description": "samsung 21s description",
            "price": 20999,
            "quantity": 6,
            "category_id": 2,
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 201
    assert all(
        key in response.json["product"]
        for key in ["id", "name", "description", "price", "quantity", "category_id"]
    )
    assert response.json["product"]["name"] == "samsung 21s"


def test_invalid_create_product(test_client, init_db, sem_token):
    response_not_found_category = test_client.post(
        "/api/v1/products",
        json={
            "name": "samsung 22s",
            "description": "samsung 22s description",
            "price": 20999,
            "quantity": 6,
            "category_id": 10,
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response_not_found_category.status_code == 404
    assert response_not_found_category.json["error"] == "Category not found"

    response_valid_error = test_client.post(
        "/api/v1/products",
        json={
            "description": "samsung 22s description",
            "price": 20999,
            "quantity": 6,
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response_valid_error.status_code == 422
    assert response_valid_error.json["error"] == "Validation error"


def test_get_products(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/products",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert "products" in response.json
    assert isinstance(response.json["products"], list)
    assert all(
        key in response.json["products"][0]
        for key in ("id", "name", "description", "price", "quantity", "category_id")
    )


def test_get_products_internal_error(test_client, init_db, sem_token):
    with patch(
        "app.api.products.crud.get_products", side_effect=Exception("Database error")
    ):
        response = test_client.get(
            "/api/v1/products",
            headers={"Authorization": f"Bearer {sem_token[0]}"},
        )
        assert response.status_code == 500

        assert "error" in response.json
        assert response.json["error"] == "Internal Server Error. Try again later"


def test_get_product_by_id(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/products/1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert "product" in response.json
    assert all(
        key in response.json["product"]
        for key in ("id", "name", "description", "price", "quantity", "category_id")
    )


def test_product_not_found(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/products/10",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 404
    assert response.json["error"] == "Product not found"


def test_update_product(test_client, init_db, sem_token):
    response = test_client.patch(
        "/api/v1/products/1",
        json={
            "description": "samsung 21s description SALE",
            "price": 15000,
            "quantity": 3,
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert "product" in response.json
    assert response.json["product"]["description"] == "samsung 21s description SALE"
    assert response.json["product"]["price"] == 15000
    assert response.json["product"]["quantity"] == 3


def test_delete_product(test_client, init_db, sem_token):
    response = test_client.delete(
        "/api/v1/products/1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 204
