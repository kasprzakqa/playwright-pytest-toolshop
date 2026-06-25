"""Shared fixtures only - no test logic here."""

import json

import pytest
from playwright.sync_api import APIRequestContext, Browser, Page, Playwright

from data.factories import Customer, make_customer
from utils import config
from utils.api_client import AuthClient, CatalogClient, ProductsClient


@pytest.fixture(scope="session", autouse=True)
def _configure_test_id(playwright: Playwright) -> None:
    """Toolshop exposes hooks via data-test, so get_by_test_id targets that attribute."""
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture(scope="session")
def base_url() -> str:
    """Override pytest-playwright's base_url so page.goto('/') is env-driven."""
    return config.BASE_URL


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return config.API_BASE_URL


@pytest.fixture
def api_context(playwright: Playwright, api_base_url: str) -> APIRequestContext:
    context = playwright.request.new_context(base_url=api_base_url)
    yield context
    context.dispose()


@pytest.fixture
def products_client(api_context: APIRequestContext) -> ProductsClient:
    return ProductsClient(api_context)


@pytest.fixture
def catalog_client(api_context: APIRequestContext) -> CatalogClient:
    return CatalogClient(api_context)


@pytest.fixture
def auth_client(api_context: APIRequestContext) -> AuthClient:
    return AuthClient(api_context)


@pytest.fixture(scope="session")
def registered_customer(playwright: Playwright, api_base_url: str) -> Customer:
    """Register a fresh customer via the API so logged-in flows never depend on (or lock) the
    shared demo account."""
    customer = make_customer()
    request = playwright.request.new_context(base_url=api_base_url)
    response = request.post("/users/register", data=customer.as_dict())
    assert response.status == 201, response.text()
    request.dispose()
    return customer


@pytest.fixture(scope="session")
def storage_state_path(
    playwright: Playwright,
    api_base_url: str,
    tmp_path_factory,
    registered_customer: Customer,
) -> str:
    """Authenticate via the API and seed the session token directly, so logged-in flows never
    depend on the (flaky) UI login form rendering. Toolshop reads the JWT from localStorage."""
    request = playwright.request.new_context(base_url=api_base_url)
    response = request.post(
        "/users/login",
        data={"email": registered_customer.email, "password": registered_customer.password},
    )
    assert response.status == 200, response.text()
    token = response.json()["access_token"]
    request.dispose()

    state = {
        "cookies": [],
        "origins": [
            {"origin": config.BASE_URL, "localStorage": [{"name": "auth-token", "value": token}]}
        ],
    }
    path = tmp_path_factory.mktemp("auth") / "customer.json"
    path.write_text(json.dumps(state))
    return str(path)


@pytest.fixture
def logged_in_page(browser: Browser, base_url: str, storage_state_path: str) -> Page:
    """A page already authenticated as the customer - no click-through login per test."""
    context = browser.new_context(base_url=base_url, storage_state=storage_state_path)
    page = context.new_page()
    yield page
    context.close()
