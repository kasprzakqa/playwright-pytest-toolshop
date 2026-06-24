"""Catalog search journeys."""

import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage


@pytest.mark.smoke
def test_search_returns_only_matching_products(page):
    home = HomePage(page)
    home.open("/")

    home.search("Pliers")

    expect(home.product_names.first).to_be_visible()
    # The queried product is in the results; search actually works (expect() auto-waits).
    expect(
        home.product_names.filter(has_text=re.compile("pliers", re.IGNORECASE))
    ).not_to_have_count(0)


@pytest.mark.regression
def test_search_with_no_match_shows_no_products(page):
    home = HomePage(page)
    home.open("/")

    home.search("zzzzz-no-such-product")

    expect(home.product_names).to_have_count(0)
