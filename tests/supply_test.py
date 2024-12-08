def test_create_supply(test_client, init_db, sem_token):
    response = test_client.post(
        "/api/v1/supplies",
        json={
            "product_name": "iphone 15 pro max",
            "quantity": 14,
            "price": 54999,
            "supplier_id": 1,
            "delivery_date": "2024-12-12",
            "status": "pending",
        },
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 201
    assert "supply" in response.json
    assert response.json["supply"] != {}


def test_get_supplys(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/supplies",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json["supplies"], list)
    assert response.json["supplies"] != []
    assert len(response.json["supplies"]) > 1


def test_get_supply_by_id(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/supplies/3",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["supply"]["product_name"] == "iphone 15 pro max"
    assert response.json["supply"]["quantity"] == 14
    assert response.json["supply"]["price"] == 54999
    assert response.json["supply"]["status"] == "pending"


def test_update_supply(test_client, init_db, sem_token):
    response = test_client.patch(
        "/api/v1/supplies/3",
        json={"status": "delivery"},
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["supply"]["status"] == "delivery"


def test_delete_supply(test_client, init_db, sem_token):
    response = test_client.delete(
        "/api/v1/supplies/3",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 204
