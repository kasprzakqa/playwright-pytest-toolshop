"""Authentication API. Token issuance on valid login, 401 on bad credentials."""

import pytest

from data.factories import make_customer
from data.models import LoginResponse, RegisteredUser

UNKNOWN_EMAIL = "not-registered@example.test"


@pytest.mark.api
@pytest.mark.smoke
def test_login_with_valid_credentials_returns_token(auth_client, registered_customer):
    resp = auth_client.login(registered_customer.email, registered_customer.password)

    assert resp.status == 200, resp.text()
    token = LoginResponse.model_validate(resp.json())
    assert token.access_token
    assert token.token_type.lower() == "bearer"


@pytest.mark.api
@pytest.mark.regression
def test_login_with_unknown_credentials_is_unauthorized(auth_client):
    resp = auth_client.login(UNKNOWN_EMAIL, "wrong-password")

    assert resp.status == 401


@pytest.mark.api
@pytest.mark.regression
def test_register_new_customer_succeeds(auth_client):
    customer = make_customer()

    resp = auth_client.register(customer.as_dict())

    assert resp.status == 201, resp.text()
    user = RegisteredUser.model_validate(resp.json())
    assert user.email == customer.email
    assert user.id


@pytest.mark.api
@pytest.mark.regression
def test_register_without_required_fields_is_rejected(auth_client):
    resp = auth_client.register({})

    assert resp.status == 422
    assert "first_name" in resp.json()


@pytest.mark.api
@pytest.mark.regression
def test_register_with_existing_email_is_rejected(auth_client):
    customer = make_customer()
    assert auth_client.register(customer.as_dict()).status == 201

    duplicate = auth_client.register(customer.as_dict())

    assert duplicate.status == 409
    assert "email" in duplicate.json()
