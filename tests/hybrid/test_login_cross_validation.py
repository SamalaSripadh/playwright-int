import pytest
from playwright.sync_api import expect

from api.account_api import AccountApi
from config.config import API_BASE_URL
from pages.login_page import LoginPage


def api_account_payload(data):
    return {
        "name": data["name"],
        "email": data["email"],
        "password": data["password"],
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "1",
        "birth_year": "1990",
        "firstname": data["first_name"],
        "lastname": data["last_name"],
        "company": data["name"],
        "address1": data["address"],
        "address2": data["address"],
        "country": data["country"],
        "zipcode": data["zipcode"],
        "state": data["state"],
        "city": data["city"],
        "mobile_number": data["mobile_number"],
    }


@pytest.mark.sanity
def test_api_registration_can_login_through_ui(page, registration_data):
    account_api = AccountApi(API_BASE_URL)
    account = api_account_payload(registration_data)
    create_response = account_api.create_account(account)
    assert create_response.status_code == 200
    assert create_response.json()["responseCode"] == 201

    try:
        login = LoginPage(page)
        login.go_to_url("/login")
        login.enter_email(registration_data["email"])
        login.enter_password(registration_data["password"])
        login.click_login()

        expect(login.is_logged_in_visible()).to_be_visible()
    finally:
        account_api.delete_account(
            account["email"], account["password"]
        )