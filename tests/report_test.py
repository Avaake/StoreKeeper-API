def test_get_sales_report_no_params(test_client, init_db):
    response = test_client.get(
        "/api/v1/reports/sales",
    )
    assert response.status_code == 200
    assert "total_sales" in response.json
    assert "total_orders" in response.json
    assert isinstance(response.json["total_sales"], int)
    assert isinstance(response.json["total_orders"], int)
    assert response.json["best_selling_products"] != {}
    assert isinstance(response.json["best_selling_products"], list)


def test_get_sales_report_product_id(test_client, init_db):
    response = test_client.get(
        "/api/v1/reports/sales",
        headers={"product_id": 5},
    )
    assert response.status_code == 200
