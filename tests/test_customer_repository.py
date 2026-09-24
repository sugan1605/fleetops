import pytest

from app.database import get_connection
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository


@pytest.fixture
def repository(monkeypatch):
    monkeypatch.setenv("FLEETOPS_DB_NAME", "fleetops_test")
    repository = CustomerRepository()

    yield repository

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM customers;")


def create_customer(customer_id: str = "PA-5054"):
    return Customer(
        customer_id=customer_id,
        customer_type="PARTNER",
        first_name="Losugan",
        last_name="Sivasuthan",
        email=f"{customer_id}@test.no",
        phone_number=f"+47 2139{customer_id}[-4:]",
    )


def test_add_customer_and_get_by_id(repository):
    customer = create_customer("PA-5042")

    repository.add(customer)

    customer_by_id = repository.get_by_id(customer.customer_id)

    assert customer_by_id == customer


def test_get_customer_by_id_returns_none_when_not_found(repository):
    result = repository.get_by_id(customer_id="PA-9999")

    assert result is None


def test_get_all_customers(repository):
    customer_1 = create_customer("PA-5043")
    customer_2 = create_customer("PA-5020")

    repository.add(customer_1)
    repository.add(customer_2)

    customers = repository.get_all()

    assert customers == [customer_1, customer_2]
