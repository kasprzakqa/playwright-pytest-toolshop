"""Checkout wizard page object: cart -> logged-in step -> billing address -> payment."""

from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    PATH = "/checkout"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.cart_total = page.get_by_test_id("cart-total")
        self.proceed_from_cart_button = page.get_by_test_id("proceed-1")
        self.proceed_from_login_button = page.get_by_test_id("proceed-2")
        self.proceed_from_address_button = page.get_by_test_id("proceed-3")
        self.street = page.get_by_test_id("street")
        self.house_number = page.get_by_test_id("house_number")
        self.city = page.get_by_test_id("city")
        self.state = page.get_by_test_id("state")
        self.country = page.get_by_test_id("country")
        self.postal_code = page.get_by_test_id("postal_code")
        self.payment_method = page.get_by_test_id("payment-method")
        self.confirm_button = page.get_by_test_id("finish")
        self.success_message = page.get_by_test_id("payment-success-message")

    def open(self) -> None:
        super().open(self.PATH)

    def proceed_from_cart(self) -> None:
        self.proceed_from_cart_button.click()

    def confirm_logged_in_step(self) -> None:
        self.proceed_from_login_button.click()

    def fill_billing_address(
        self,
        *,
        street: str,
        house_number: str,
        city: str,
        state: str,
        country: str,
        postal_code: str,
    ) -> None:
        self.street.fill(street)
        self.house_number.fill(house_number)
        self.city.fill(city)
        self.state.fill(state)
        self.country.select_option(label=country)
        self.postal_code.fill(postal_code)

    def proceed_from_address(self) -> None:
        self.proceed_from_address_button.click()

    def pay_with(self, method: str) -> None:
        self.payment_method.select_option(label=method)
        self.confirm_button.click()
