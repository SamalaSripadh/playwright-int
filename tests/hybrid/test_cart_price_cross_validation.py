import json

import pytest
from playwright.sync_api import expect

from api.products_api import ProductsApi
from config.config import API_BASE_URL
from pages.cart_page import CartPage
from pages.products_page import ProductsPage


with open("data/ui_data.json", encoding="utf-8") as file:
    ui_data = json.load(file)


@pytest.mark.sanity
def test_ui_cart_prices_match_api_products(page):
    products_page = ProductsPage(page)
    products_page.go_to_products_page()
    products_page.add_product_to_cart(ui_data["known_product"])
    products_page.continue_shopping()
    products_page.add_product_to_cart(ui_data["second_product"])
    products_page.click_cart()
    cart = CartPage(page)
    api_products = ProductsApi(API_BASE_URL).get_products().json()["products"]
    products_by_id = {str(product["id"]): product for product in api_products}

    for product_name in (ui_data["known_product"], ui_data["second_product"]):
        product_id = cart.product_id(product_name)
        ui_price = cart.product_price(product_name)
        assert product_id in products_by_id
        assert ui_price == products_by_id[product_id]["price"]
        expect(cart.is_product_visible(product_name)).to_be_visible()


@pytest.mark.regression
def test_ui_search_results_match_api_search(page):
    products_page = ProductsPage(page)
    products_page.go_to_products_page()
    products_page.search_product(ui_data["known_product"])
    ui_names = products_page.visible_product_names()
    api_response = ProductsApi(API_BASE_URL).search_product(ui_data["known_product"])
    api_names = [product["name"] for product in api_response.json()["products"]]

    assert sorted(ui_names) == sorted(api_names)
