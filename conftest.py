import json
import os

import pytest
from faker import Faker
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config.config import AUTH_EMAIL, AUTH_FILE, AUTH_PASSWORD, BASE_URL
from pages.login_page import LoginPage

with open("data/ui_data.json", encoding="utf-8") as file:
    UI_DATA = json.load(file)


def pytest_addoption(parser):
    parser.addini("headed", "run Playwright tests with a visible browser", type="bool", default=False)
    parser.addini(
        "tracing",
        "Playwright tracing mode: off, on, or retain-on-failure",
        default="retain-on-failure",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    if call.when == "call":
        item.rep_call = outcome.get_result()


def _trace_file(request):
    trace_dir = os.path.join("test-results", "traces")
    os.makedirs(trace_dir, exist_ok=True)
    test_name = request.node.nodeid.replace("/", "_").replace("\\", "_").replace(":", "_")
    worker_id = os.getenv("PYTEST_XDIST_WORKER", "master")
    return os.path.join(trace_dir, f"{worker_id}_{test_name}.zip")


def _start_tracing(context, request):
    mode = request.config.getini("tracing").lower()
    if mode not in {"off", "on", "retain-on-failure"}:
        raise pytest.UsageError("tracing must be off, on, or retain-on-failure")
    if mode != "off":
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
    return mode


def _stop_tracing(context, request, mode):
    if mode == "off":
        return
    failed = getattr(request.node, "rep_call", None)
    if mode == "on" or (failed and failed.failed):
        context.tracing.stop(path=_trace_file(request))
    else:
        context.tracing.stop()


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
def context(browser: Browser, request) -> BrowserContext:
    """Provide an isolated browser context for each test."""
    context = browser.new_context(
        base_url=BASE_URL,
        viewport={"width": 1920, "height": 1080},
    )
    trace_mode = _start_tracing(context, request)
    yield context
    _stop_tracing(context, request, trace_mode)
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Provide a fresh page for each test."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="session")
def authenticated_state(browser: Browser) -> str:
    if not AUTH_EMAIL or not AUTH_PASSWORD:
        raise pytest.UsageError("AUTH_EMAIL and AUTH_PASSWORD must be set in .env")

    auth_file = AUTH_FILE
    worker_id = os.getenv("PYTEST_XDIST_WORKER")
    if worker_id:
        auth_root, auth_name = os.path.split(AUTH_FILE)
        auth_file = os.path.join(auth_root, f"{worker_id}_{auth_name}")

    auth_dir = os.path.dirname(auth_file)
    if auth_dir:
        os.makedirs(auth_dir, exist_ok=True)
    if os.path.exists(auth_file):
        return auth_file

    context = browser.new_context(
        base_url=BASE_URL,
        viewport={"width": 1920, "height": 1080},
    )
    page = context.new_page()
    page.goto("/login", wait_until="domcontentloaded")
    login = LoginPage(page)
    login.enter_email(AUTH_EMAIL)
    login.enter_password(AUTH_PASSWORD)
    login.click_login()
    login.is_logged_in_visible().wait_for(state="visible")
    context.storage_state(path=auth_file)
    context.close()
    return auth_file


@pytest.fixture(scope="function")
def auth_context(browser: Browser, authenticated_state: str, request) -> BrowserContext:
    context = browser.new_context(
        base_url=BASE_URL,
        viewport={"width": 1920, "height": 1080},
        storage_state=authenticated_state,
    )
    trace_mode = _start_tracing(context, request)
    yield context
    _stop_tracing(context, request, trace_mode)
    context.close()


@pytest.fixture(scope="function")
def auth_page(auth_context: BrowserContext) -> Page:
    page = auth_context.new_page()
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