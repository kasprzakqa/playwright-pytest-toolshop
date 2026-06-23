"""Authentication journeys."""

import re

import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage

UNKNOWN_EMAIL = "not-registered@example.test"


@pytest.mark.smoke
def test_login_with_valid_credentials_redirects_to_account(page, registered_customer):
    login = LoginPage(page)
    login.open()

    login.login(registered_customer.email, registered_customer.password)

    expect(page).to_have_url(re.compile(r"/account"))


@pytest.mark.regression
def test_login_with_invalid_credentials_shows_error(page):
    login = LoginPage(page)
    login.open()

    login.login(UNKNOWN_EMAIL, "wrong-password")

    expect(login.error).to_be_visible()
    expect(login.error).to_contain_text("Invalid")
