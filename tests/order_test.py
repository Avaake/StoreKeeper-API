def test_valid_create_order(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/orders",
        json={
            "products": [
                {"product_id": 1, "quantity": 4},
                {"product_id": 2, "quantity": 1},
            ]
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert response.json["order"]["status"] == "pending"
    assert isinstance(response.json["order"]["order_items"], list)
    assert response.json["order"]["order_items"] != []
    assert "product_id" in response.json["order"]["order_items"][0]
    assert "product_name" in response.json["order"]["order_items"][0]
    assert "quantity" in response.json["order"]["order_items"][0]
    assert "price" in response.json["order"]["order_items"][0]


def test_invalid_create_order(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/orders",
        json={
            "products": [
                {"product_id": "ads", "quantity": 0},
            ]
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 422
    assert response.json["error"] == "Validation error"
    assert "details" in response.json
    assert len(response.json["details"]) != 0


def test_insufficient_stock_quantity_error(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/orders",
        json={
            "products": [
                {"product_id": 1, "quantity": 20},
            ]
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 400
    assert (
        response.json["error"]
        == "Insufficient quantity of product. Available: 7, required: 20"
    )


def test_create_order_with_invalid_product_id(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/orders",
        json={
            "products": [
                {"product_id": 10, "quantity": 2},
            ]
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 404
    assert response.json["error"] == "404 Not Found: Product not found"


def test_get_all_products(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/orders",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json["orders"], list)
    assert response.json["orders"] != []


def test_get_order_by_id(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/orders/1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json["order"], dict)
    assert response.json["order"] != {}
    assert response.json["order"]["id"] == 1


def test_update_order(test_client, init_db, sem_token):
    response = test_client.patch(
        "/api/v1/orders/1",
        json={
            "products": [
                {"product_id": 1, "quantity": 7},
                {"product_id": 2, "quantity": 2},
            ]
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json["order"], dict)
    assert response.json["order"] != {}
    assert response.json["order"]["id"] == 1
    order_items = response.json["order"]["order_items"]

    product_1 = next(item for item in order_items if item["product_id"] == 1)
    product_2 = next(item for item in order_items if item["product_id"] == 2)

    assert product_1["quantity"] == 7
    assert product_2["quantity"] == 2


def test_update_order_invalid_status(test_client, init_db, sem_token):
    response = test_client.patch(
        "/api/v1/orders/1",
        json={"status": "deleted"},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 422
    assert response.json["error"] == "Validation error"
    assert "details" in response.json
    assert response.json["details"] != {}


def test_delete_order(test_client, init_db, sem_token):
    response = test_client.delete(
        "/api/v1/orders/2",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 204
