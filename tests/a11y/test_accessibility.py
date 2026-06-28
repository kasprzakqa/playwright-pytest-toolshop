"""Accessibility: automated axe scan (gated on serious/critical) + keyboard operability."""

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import expect

from pages.home_page import HomePage

axe = Axe()
BLOCKING = ("serious", "critical")


@pytest.mark.regression
@pytest.mark.a11y
def test_home_has_no_serious_accessibility_violations(page):
    home = HomePage(page)
    home.open("/")
    home.search_input.wait_for()

    results = axe.run(page)
    blocking = [v for v in results.response["violations"] if v["impact"] in BLOCKING]

    assert not blocking, "serious/critical a11y violations: " + ", ".join(
        f"{v['id']} ({v['impact']})" for v in blocking
    )


@pytest.mark.regression
@pytest.mark.a11y
def test_search_is_keyboard_operable(page):
    home = HomePage(page)
    home.open("/")

    home.search_input.focus()
    expect(home.search_input).to_be_focused()
    home.search_input.press_sequentially("Pliers")
    page.keyboard.press("Enter")

    expect(home.product_names.first).to_be_visible()
