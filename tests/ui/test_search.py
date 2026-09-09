import json

import pytest
from playwright.sync_api import expect

from pages.products_page import ProductsPage


with open("data/ui_data.json", encoding="utf-8") as file:
    ui_data = json.load(file)


@pytest.mark.sanity
def test_search_results_contain_known_product(page):
    pp = ProductsPage(page)
    pp.go_to_products_page()
    pp.search_product(ui_data["known_product"])

    expect(pp.is_products_title_visible()).to_be_visible()
    expect(pp.are_search_results_visible()).to_be_visible()


@pytest.mark.regression
def test_search_with_no_matches_shows_empty_state(page):
    pp = ProductsPage(page)
    pp.go_to_products_page()
    pp.search_product(ui_data["missing_product"])

    expect(pp.is_empty_state_visible()).to_be_visible()