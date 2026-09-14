import pytest
from datetime import datetime


from app.models.rental import Rental
from app.models.customer import Customer
from app.models.vehicle import Vehicle


@pytest.fixture
def test_customer():
    return Customer(
        customer_id="PA-5052",
        customer_type="PARTNER",
        first_name="Lars",
        last_name="Monsen",
        phone_number="+4712345678",
        email="test1test@gmail.com",
    )


@pytest.fixture
def test_vehicle():
    return Vehicle(
        registration_number="SX 503335",
        make="Volvo",
        model="XC-60",
        fuel_type="Petrol",
    )


def test_rental_can_be_created(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0),
        due=datetime(2026, 9, 17, 17, 0),
        status="ACTIVE",
    )

    assert rental.customer is test_customer
    assert rental.vehicle is test_vehicle
    assert rental.start == datetime(2026, 9, 15, 17, 0)
    assert rental.due == datetime(2026, 9, 17, 17, 0)
    assert rental.status == "ACTIVE"


def test_rental_invalid_status(test_customer, test_vehicle):
    with pytest.raises(ValueError):
        Rental(
            test_customer,
            test_vehicle,
            start=datetime(2026, 9, 15, 17, 0),
            due=datetime(2026, 9, 16, 17, 0),
            status="INVALID",
        )


def test_rental_due_date_cannot_be_before_start_date(test_customer, test_vehicle):
    with pytest.raises(ValueError):
        Rental(
            test_customer,
            test_vehicle,
            start=datetime(2026, 9, 15, 17, 0),
            due=datetime(2026, 9, 14, 17, 0),
            status="ACTIVE",
        )


def test_active_rental_can_register_return(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 14, 21, 0),
        due=datetime(2026, 9, 15, 21, 0),
        status="ACTIVE",
    )

    rental.register_return(datetime(2026, 9, 15, 19, 30))

    assert rental.return_time == datetime(2026, 9, 15, 19, 30)


def test_non_active_rental_cannot_register_return(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 14, 21, 0),
        due=datetime(2026, 9, 15, 21, 0),
        status="COMPLETED",
    )

    with pytest.raises(ValueError):
        rental.register_return(datetime(2026, 9, 15, 19, 30))

    assert rental.return_time is None


def test_return_cannot_be_before_rental_start(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 14, 17, 0),
        due=datetime(2026, 9, 15, 17, 0),
        status="ACTIVE",
    )

    with pytest.raises(ValueError):
        rental.register_return(datetime(2026, 9, 13, 17, 0))

    assert rental.return_time is None
