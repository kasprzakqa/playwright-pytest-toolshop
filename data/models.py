"""Typed API contracts. Validating against these makes a renamed/missing field fail loudly."""

from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class _Model(BaseModel):
    model_config = ConfigDict(extra="ignore")


class Product(_Model):
    id: str
    name: str
    price: float
    is_location_offer: bool
    is_rental: bool
    description: str | None = None


class Category(_Model):
    id: str
    name: str
    slug: str
    parent_id: str | None = None


class Brand(_Model):
    id: str
    name: str
    slug: str


class Paginated(_Model, Generic[T]):
    current_page: int
    data: list[T]
    last_page: int
    per_page: int
    total: int


class LoginResponse(_Model):
    access_token: str
    token_type: str
    expires_in: int


class RegisteredUser(_Model):
    id: str
    first_name: str
    last_name: str
    email: str
