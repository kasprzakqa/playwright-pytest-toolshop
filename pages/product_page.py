"""Product detail page object."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductDetailPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.add_to_cart_button = page.get_by_test_id("add-to-cart")
        self.product_name = page.get_by_test_id("product-name")
        self.unit_price = page.get_by_test_id("unit-price")

    def open(self, product_id: str) -> None:
        super().open(f"/product/{product_id}")

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()
        # Wait for the cart badge to reflect the add before navigating onward (avoids a race).
        self.page.wait_for_function(
            "() => /[1-9]/.test("
            "document.querySelector('[data-test=\"cart-quantity\"]')?.textContent || '')"
        )
