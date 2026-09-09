import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage


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


@pytest.mark.smoke
def test_valid_login(page, registration_data):
    create_account(page, registration_data)
    lp = LoginPage(page)
    lp.click_logout()
    lp.enter_email(registration_data["email"])
    lp.enter_password(registration_data["password"])
    lp.click_login()

    expect(lp.is_logged_in_visible()).to_be_visible()


@pytest.mark.regression
def test_invalid_login(page, registration_data):
    lp = LoginPage(page)
    lp.go_to_url("/login")
    lp.enter_email(registration_data["email"])
    lp.enter_password(registration_data["password"])
    lp.click_login()

    expect(lp.is_invalid_login_error_visible()).to_be_visible()


@pytest.mark.sanity
def test_logout_returns_to_logged_out_state(page, registration_data):
    create_account(page, registration_data)
    lp = LoginPage(page)
    lp.click_logout()

    expect(lp.is_login_form_visible()).to_be_visible()