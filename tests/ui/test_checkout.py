import json

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.products_page import ProductsPage
from pages.signup_page import SignupPage
from pages.subscription_page import SubscriptionPage


with open("data/ui_data.json", encoding="utf-8") as file:
    ui_data = json.load(file)


def create_account(page, data):
    sp = SignupPage(page)
    sp.go_to_signup_page()
    sp.enter_signup_name(data["name"])
    sp.enter_signup_email(data["email"])
    sp.click_signup()
    sp.select_gender(data["gender"])
    sp.enter_password(data["password"])
    sp.enter_first_name(data["first_name"])
    sp.enter_last_name(data["last_name"])
    sp.enter_address(data["address"])
    sp.select_country(data["country"])
    sp.enter_state(data["state"])
    sp.enter_city(data["city"])
    sp.enter_zipcode(data["zipcode"])
    sp.enter_mobile_number(data["mobile_number"])
    sp.click_create_account()
    sp.click_continue()


@pytest.mark.sanity
def test_checkout_summary_matches_cart_product(auth_page):
    page = auth_page
    pp = ProductsPage(page)
    pp.go_to_products_page()
    pp.add_product_to_cart(ui_data["known_product"])
    pp.click_cart()
    cp = CartPage(page)
    cp.click_checkout()
    checkout = CheckoutPage(page)

    expect(checkout.is_address_details_visible()).to_be_visible()
    expect(checkout.is_order_review_visible()).to_be_visible()
    expect(checkout.is_product_in_order_visible(ui_data["known_product"])).to_be_visible()


@pytest.mark.regression
def test_subscribe_to_newsletter(page, registration_data):
    pp = ProductsPage(page)
    pp.go_to_products_page()
    subscription = SubscriptionPage(page)
    subscription.enter_email(registration_data["email"])
    subscription.click_subscribe()

    expect(subscription.is_success_message_visible()).to_be_visible()