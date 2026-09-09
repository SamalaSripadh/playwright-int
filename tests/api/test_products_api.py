import json

import pytest

from api.products_api import ProductsApi
from config.config import API_BASE_URL


with open("data/api_data.json", encoding="utf-8") as file:
    api_data = json.load(file)


@pytest.fixture
def products_api():
    return ProductsApi(API_BASE_URL)


@pytest.mark.smoke
def test_get_all_products(products_api):
    response = products_api.get_products()
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert body["products"]
    for product in body["products"]:
        assert isinstance(product["id"], int)
        assert isinstance(product["name"], str)
        assert isinstance(product["price"], str)
        assert isinstance(product["category"], dict)
        assert isinstance(product["category"]["usertype"]["usertype"], str)
        assert isinstance(product["category"]["category"], str)


@pytest.mark.sanity
def test_search_known_product(products_api):
    response = products_api.search_product(api_data["known_product"])
    body = response.json()

    assert response.status_code == 200
    assert body["responseCode"] == 200
    assert any(
        api_data["known_product"].lower() == product["name"].lower()
        for product in body["products"]
    )


@pytest.mark.regression
def test_unsupported_products_method_returns_405(products_api):
    response = products_api.update_products()

    assert response.status_code == 200
    assert response.json()["responseCode"] == 405