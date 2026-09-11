from app.customer import Customer

import pytest


def test_customer_creation():
    customer = Customer(
        customer_id="PA-5054",
        customer_type="PARTNER",
        first_name="Losugan",
        last_name="Sivasuthan",
        email="test@test.no",
        phone_number="+47 21390016",
    )

    assert customer.customer_id == "PA-5054"
    assert customer.customer_type == "PARTNER"
    assert customer.first_name == "Losugan"
    assert customer.last_name == "Sivasuthan"
    assert customer.email == "test@test.no"
    assert customer.phone_number == "+47 21390016"


def test_customer_rejects_invalid_customer_type():
    with pytest.raises(ValueError):
        Customer(
            customer_id="W-1002",
            customer_type="VACATION",
            first_name="Mona",
            last_name="Lisa",
            email="test4@gmail.com",
            phone_number="+49243434324",
        )


def test_customer_id_must_match_customer_type():
    with pytest.raises(ValueError):
        Customer(
            customer_id="LE-5024",
            customer_type="PARTNER",
            first_name="Ola",
            last_name="Normann",
            email="test3@gmail.com",
            phone_number="+4721213232",
        )


def test_customer_id_must_match_business_type():
    with pytest.raises(ValueError):
        Customer(
            customer_id="LE-5054",
            customer_type="BUSINESS",
            first_name="Ola",
            last_name="Normann",
            email="test4@gmail.com",
            phone_number="+39002451525"
        )        