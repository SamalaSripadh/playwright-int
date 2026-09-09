import json

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.signup_page import SignupPage


with open("data/ui_data.json", encoding="utf-8") as file:
    ui_data = json.load(file)


def complete_registration(page, data):
    sp = SignupPage(page)
    sp.go_to_signup_page()
    sp.enter_signup_name(data["name"])
    sp.enter_signup_email(data["email"])
    sp.click_signup()
    sp.select_gender(data["gender"])
    sp.enter_password(data["password"])
    sp.enter_first_name(data["first_name"])
    sp.enter_last_name(data["last_name"])
    sp.select_date_of_birth(
        ui_data["registration_day"],
        ui_data["registration_month"],
        ui_data["registration_year"],
    )
    sp.enter_address(data["address"])
    sp.select_country(ui_data["registration_country"])
    sp.enter_state(data["state"])
    sp.enter_city(data["city"])
    sp.enter_zipcode(data["zipcode"])
    sp.enter_mobile_number(data["mobile_number"])
    sp.click_create_account()


@pytest.mark.smoke
def test_home_page_loads(page):
    hp = HomePage(page)
    hp.go_to_home_page()

    expect(hp.is_header_visible()).to_be_visible()
    expect(hp.is_navbar_visible()).to_be_visible()
    expect(hp.is_footer_visible()).to_be_visible()


@pytest.mark.smoke
def test_user_registration(page, registration_data):
    complete_registration(page, registration_data)

    expect(SignupPage(page).is_account_created_visible()).to_be_visible()


@pytest.mark.regression
def test_registration_fails_for_existing_email(page, registration_data):
    complete_registration(page, registration_data)
    page.goto("/login")
    LoginPage(page).click_logout()
    sp = SignupPage(page)
    sp.enter_signup_name(registration_data["name"])
    sp.enter_signup_email(registration_data["email"])
    sp.click_signup()

    expect(sp.is_existing_email_error_visible()).to_be_visible()


@pytest.mark.regression
def test_registration_form_requires_email(page, registration_data):
    sp = SignupPage(page)
    sp.go_to_signup_page()
    sp.enter_signup_name(registration_data["name"])
    sp.click_signup()

    expect(sp.is_signup_form_visible()).to_be_visible()