"""Checkout journey: the crown-jewel path - add to cart, bill, pay, confirmation."""

import re

import pytest
from playwright.sync_api import expect

from pages.checkout_page import CheckoutPage
from pages.home_page import HomePage
from pages.product_page import ProductDetailPage


@pytest.mark.smoke
def test_checkout_with_cash_on_delivery_succeeds(logged_in_page):
    home = HomePage(logged_in_page)
    home.open("/")
    home.search("Pliers")  # a reliably in-stock product, so add-to-cart is enabled
    home.open_first_product()

    product = ProductDetailPage(logged_in_page)
    expect(product.unit_price).to_be_visible()
    amount = re.search(r"[\d.]+", product.unit_price.inner_text()).group()
    product.add_to_cart()

    checkout = CheckoutPage(logged_in_page)
    checkout.open()
    # Cart total must reflect the item price for a single-item cart, not a silently zeroed total.
    expect(checkout.cart_total).to_contain_text(amount)

    checkout.proceed_from_cart()
    checkout.confirm_logged_in_step()
    checkout.fill_billing_address(
        street="Main Street 1",
        house_number="12",
        city="Wroclaw",
        state="Dolnoslaskie",
        country="Poland",
        postal_code="50-001",
    )
    checkout.proceed_from_address()
    checkout.pay_with("Cash on Delivery")

    expect(checkout.success_message).to_have_text("Payment was successful")
