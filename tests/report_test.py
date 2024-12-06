from unittest.mock import patch


def test_get_sales_report_no_params(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/reports/sales",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert "total_sales" in response.json
    assert "total_orders" in response.json
    assert isinstance(response.json["total_sales"], int)
    assert isinstance(response.json["total_orders"], int)
    assert response.json["best_selling_products"] != {}
    assert isinstance(response.json["best_selling_products"], list)
    assert response.json["total_sales"] == 188000


def test_get_sales_report_product_id(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/reports/sales?product_id=1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["total_sales"] == 120000


def test_get_sales_report_category_id(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/reports/sales?category_id=1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )
    assert response.status_code == 200
    assert response.json["total_sales"] == 160000
    assert response.json["best_selling_products"][0]["name"] == "macbook air"


def test_get_sales_internal_error(test_client, init_db, sem_token):
    with patch(
        "app.api.reports.utils.calculate_sales_report",
        side_effect=Exception("Internal Server Error"),
    ):
        response = test_client.get(
            "/api/v1/reports/sales",
            headers={"Authorization": f"Bearer {sem_token[0]}"},
        )
        assert response.status_code == 500
        assert "error" in response.json
        assert response.json["error"] == "Internal Server Error. Try again later"


def test_get_products_that_end(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/reports/inventory",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert (
        response.json["message"] == "Products in short supply retrieved successfully."
    )
    assert isinstance(response.json["products"], list)
    assert response.json["products"][0]["quantity"] < 15


def test_get_products_that_end_category_id(test_client, init_db, sem_token):
    response = test_client.get(
        "/api/v1/reports/inventory?category_id=1",
        headers={"Authorization": f"Bearer {sem_token[0]}"},
    )

    assert response.status_code == 200
    assert (
        response.json["message"] == "Products in short supply retrieved successfully."
    )
    assert isinstance(response.json["products"], list)
    assert response.json["products"][0]["name"] == "macbook air"
    assert response.json["products"][0]["quantity"] == 11


def test_get_products_that_end_internal_error(test_client, init_db, sem_token):
    with patch(
        "app.api.reports.utils.list_of_items_in_short_supply",
        side_effect=Exception("Internal Server Error"),
    ):
        response = test_client.get(
            "/api/v1/reports/inventory?category_id=1",
            headers={"Authorization": f"Bearer {sem_token[0]}"},
        )

        assert response.status_code == 500
        assert "error" in response.json
        assert response.json["error"] == "Internal Server Error. Try again later"
