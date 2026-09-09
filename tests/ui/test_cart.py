import json

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.products_page import ProductsPage


with open("data/ui_data.json", encoding="utf-8") as file:
    ui_data = json.load(file)


@pytest.mark.smoke
def test_add_one_product_to_cart(page):
    pp = ProductsPage(page)
    pp.go_to_products_page()
    pp.add_product_to_cart(ui_data["known_product"])
    pp.click_cart()
    cp = CartPage(page)

    expect(cp.is_product_visible(ui_data["known_product"])).to_be_visible()
    assert cp.product_price(ui_data["known_product"])


@pytest.mark.sanity
def test_add_multiple_products_and_verify_quantities(page):
    pp = ProductsPage(page)
    pp.go_to_products_page()
    pp.add_product_to_cart(ui_data["known_product"])
    pp.continue_shopping()
    pp.add_product_to_cart(ui_data["second_product"])
    pp.click_cart()
    cp = CartPage(page)

    expect(cp.is_product_visible(ui_data["known_product"])).to_be_visible()
    expect(cp.is_product_visible(ui_data["second_product"])).to_be_visible()


@pytest.mark.regression
def test_remove_product_from_cart(page):
    pp = ProductsPage(page)
    pp.go_to_products_page()
    pp.add_product_to_cart(ui_data["known_product"])
    pp.click_cart()
    cp = CartPage(page)
    cp.remove_product(ui_data["known_product"])

    expect(cp.is_cart_empty_visible()).to_be_visible()