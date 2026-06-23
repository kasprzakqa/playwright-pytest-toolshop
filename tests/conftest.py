"""Shared fixtures only - no test logic here."""

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from data.factories import Customer, make_customer
from utils import config
from utils.api_client import AuthClient, CatalogClient, ProductsClient


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
