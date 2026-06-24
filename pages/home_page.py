"""Home / catalog page object."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.search_input = page.get_by_placeholder("Search")
        self.search_submit = page.get_by_test_id("search-submit")
        self.product_names = page.get_by_test_id("product-name")

    def search(self, query: str) -> None:
        self.search_input.fill(query)
        self.search_submit.click()

    def open_first_product(self) -> None:
        # FIXME: prefix selector; product card links lack a stable role+name pair to target.
        self.page.locator("a[data-test^='product-']").first.click()
