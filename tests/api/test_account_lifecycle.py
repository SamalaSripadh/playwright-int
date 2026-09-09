import json

import pytest
from faker import Faker

from api.account_api import AccountApi
from config.config import API_BASE_URL


with open("data/api_data.json", encoding="utf-8") as file:
    api_data = json.load(file)


@pytest.mark.smoke
def test_account_lifecycle():
    fake = Faker()
    account = {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(length=12),
        "title": "Mr",
        "birth_date": "1",
        "birth_month": "1",
        "birth_year": "1990",
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "company": fake.company(),
        "address1": fake.street_address(),
        "address2": fake.secondary_address(),
        "country": "Canada",
        "zipcode": fake.postcode(),
        "state": fake.state(),
        "city": fake.city(),
        "mobile_number": fake.msisdn()[-10:],
    }
    account_api = AccountApi(API_BASE_URL)

    create_response = account_api.create_account(account)
    assert create_response.status_code == 200
    assert create_response.json()["responseCode"] == 201

    login_response = account_api.verify_login(account["email"], account["password"])
    assert login_response.status_code == 200
    assert login_response.json()["responseCode"] == 200

    account["name"] = api_data["updated_name"]
    update_response = account_api.update_account(account)
    assert update_response.status_code == 200
    assert update_response.json()["responseCode"] == 200

    detail_response = account_api.get_user_detail(account["email"])
    assert detail_response.status_code == 200
    assert detail_response.json()["user"]["name"] == api_data["updated_name"]

    delete_response = account_api.delete_account(account["email"], account["password"])
    assert delete_response.status_code == 200
    assert delete_response.json()["responseCode"] == 200

    deleted_detail_response = account_api.get_user_detail(account["email"])
    assert deleted_detail_response.json()["responseCode"] == 404