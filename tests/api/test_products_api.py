"""Products / catalog API. Validates status + content-type + body schema + negative paths."""

import pytest

from data.models import Brand, Category, Paginated, Product


@pytest.mark.api
@pytest.mark.smoke
def test_list_products_returns_paginated_catalog(products_client):
    resp = products_client.list()

    assert resp.status == 200, resp.text()
    assert "application/json" in resp.headers["content-type"]

    page = Paginated[Product].model_validate(resp.json())
    assert page.current_page == 1
    assert len(page.data) > 0
    assert all(p.price >= 0 for p in page.data)


@pytest.mark.api
@pytest.mark.regression
def test_product_pagination_returns_distinct_pages(products_client):
    first = Paginated[Product].model_validate(products_client.list(page=1).json())
    second = Paginated[Product].model_validate(products_client.list(page=2).json())

    assert second.current_page == 2
    assert {p.id for p in first.data}.isdisjoint({p.id for p in second.data})


@pytest.mark.api
@pytest.mark.regression
def test_get_unknown_product_returns_404(products_client):
    resp = products_client.get("does-not-exist")

    assert resp.status == 404


@pytest.mark.api
@pytest.mark.regression
def test_categories_expose_expected_shape(catalog_client):
    resp = catalog_client.categories()

    assert resp.status == 200
    categories = [Category.model_validate(c) for c in resp.json()]
    assert any(c.name for c in categories)


@pytest.mark.api
@pytest.mark.regression
def test_brands_expose_expected_shape(catalog_client):
    resp = catalog_client.brands()

    assert resp.status == 200
    brands = [Brand.model_validate(b) for b in resp.json()]
    assert any(b.name for b in brands)
