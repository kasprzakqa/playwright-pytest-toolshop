"""Base for all page objects. Locators and actions live in subclasses, never in tests."""

from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def open(self, path: str = "/") -> None:
        self.page.goto(path)
