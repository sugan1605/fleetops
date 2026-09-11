from app.customer import Customer


def test_customer_creation():
    customer = Customer(
        customer_id=5054,
        first_name="Losugan",
        last_name="Sivasuthan",
        email="test@test.no",
        phone_number="+47 21390016",
    )

    assert customer.customer_id == 5054
    assert customer.first_name == "Losugan"
    assert customer.last_name == "Sivasuthan"
    assert customer.email == "test@test.no"
    assert customer.phone_number == "+47 21390016"
