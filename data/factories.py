"""Faker-based test-data builders. Realistic but never real PII; each test makes its own."""

from dataclasses import asdict, dataclass

from faker import Faker

_faker = Faker()


@dataclass
class Customer:
    first_name: str
    last_name: str
    email: str
    password: str

    def as_dict(self) -> dict:
        return asdict(self)


def make_customer(**overrides) -> Customer:
    """Build a unique customer; pass overrides to pin specific fields."""
    data = {
        "first_name": _faker.first_name(),
        "last_name": _faker.last_name(),
        "email": _faker.unique.email(),
        "password": "Str0ng!Pass123",
    }
    data.update(overrides)
    return Customer(**data)
