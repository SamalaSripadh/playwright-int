import json

import pytest
from faker import Faker
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config.config import BASE_URL

with open("data/ui_data.json", encoding="utf-8") as file:
    UI_DATA = json.load(file)


def pytest_addoption(parser):
    parser.addini("headed", "run Playwright tests with a visible browser", type="bool", default=False)


@pytest.fixture(scope="session")
def browser(pytestconfig) -> Browser:
    """Launch one Chromium instance for the test session."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=not pytestconfig.getini("headed")
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """Provide an isolated browser context for each test."""
    context = browser.new_context(
        base_url=BASE_URL,
        viewport={"width": 1920, "height": 1080},
    )
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Provide a fresh page for each test."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    return BASE_URL


@pytest.fixture
def registration_data():
    fake = Faker()
    return {
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password(length=12),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "address": fake.street_address(),
        "state": fake.state(),
        "city": fake.city(),
        "zipcode": fake.postcode(),
        "mobile_number": fake.msisdn()[-10:],
        "gender": UI_DATA["registration_gender"],
        "country": UI_DATA["registration_country"],
    }