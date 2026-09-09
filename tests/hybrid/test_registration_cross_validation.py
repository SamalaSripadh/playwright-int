import json

import pytest
from playwright.sync_api import expect

from api.account_api import AccountApi
from config.config import API_BASE_URL
from pages.signup_page import SignupPage


with open("data/ui_data.json", encoding="utf-8") as file:
    ui_data = json.load(file)


def complete_registration(page, data):
    signup = SignupPage(page)
    signup.go_to_signup_page()
    signup.enter_signup_name(data["name"])
    signup.enter_signup_email(data["email"])
    signup.click_signup()
    signup.select_gender(data["gender"])
    signup.enter_password(data["password"])
    signup.enter_first_name(data["first_name"])
    signup.enter_last_name(data["last_name"])
    signup.select_date_of_birth(
        ui_data["registration_day"],
        ui_data["registration_month"],
        ui_data["registration_year"],
    )
    signup.enter_address(data["address"])
    signup.select_country(data["country"])
    signup.enter_state(data["state"])
    signup.enter_city(data["city"])
    signup.enter_zipcode(data["zipcode"])
    signup.enter_mobile_number(data["mobile_number"])
    signup.click_create_account()


@pytest.mark.smoke
def test_ui_registration_exists_in_api(page, registration_data):
    complete_registration(page, registration_data)
    expect(SignupPage(page).is_account_created_visible()).to_be_visible()

    response = AccountApi(API_BASE_URL).get_user_detail(registration_data["email"])
    assert response.status_code == 200
    assert response.json()["user"]["email"] == registration_data["email"]

    AccountApi(API_BASE_URL).delete_account(
        registration_data["email"], registration_data["password"]
    )
