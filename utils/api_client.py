"""API clients over Playwright's APIRequestContext, one class per service domain."""

from playwright.sync_api import APIRequestContext, APIResponse


class ProductsClient:
    def __init__(self, context: APIRequestContext) -> None:
        self._ctx = context

    def list(self, page: int = 1) -> APIResponse:
        return self._ctx.get("/products", params={"page": page})

    def get(self, product_id: str) -> APIResponse:
        return self._ctx.get(f"/products/{product_id}")


class CatalogClient:
    def __init__(self, context: APIRequestContext) -> None:
        self._ctx = context

    def categories(self) -> APIResponse:
        return self._ctx.get("/categories")

    def brands(self) -> APIResponse:
        return self._ctx.get("/brands")


class AuthClient:
    def __init__(self, context: APIRequestContext) -> None:
        self._ctx = context

    def login(self, email: str, password: str) -> APIResponse:
        return self._ctx.post("/users/login", data={"email": email, "password": password})

    def register(self, payload: dict) -> APIResponse:
        return self._ctx.post("/users/register", data=payload)
