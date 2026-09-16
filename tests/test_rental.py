from datetime import datetime, timezone

import pytest

from app.models.customer import Customer
from app.models.rental import Rental
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
        odometer_km=8000,
    )


def test_rental_can_be_created(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 17, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    assert rental.customer is test_customer
    assert rental.vehicle is test_vehicle
    assert rental.start == datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc)
    assert rental.due == datetime(2026, 9, 17, 17, 0 , tzinfo=timezone.utc)
    assert rental.status == "ACTIVE"


def test_rental_invalid_status(test_customer, test_vehicle):
    with pytest.raises(ValueError):
        Rental(
            test_customer,
            test_vehicle,
            start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
            due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
            status="INVALID",
        )


def test_rental_due_date_cannot_be_before_start_date(test_customer, test_vehicle):
    with pytest.raises(ValueError):
        Rental(
            test_customer,
            test_vehicle,
            start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
            due=datetime(2026, 9, 14, 17, 0, tzinfo=timezone.utc),
            status="ACTIVE",
        )


def test_active_rental_can_register_return(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 14, 21, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 15, 21, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    rental.register_return(datetime(2026, 9, 15, 19, 30, tzinfo=timezone.utc))

    assert rental.return_time == datetime(2026, 9, 15, 19, 30, tzinfo=timezone.utc)


def test_non_active_rental_cannot_register_return(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 14, 21, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 15, 21, 0, tzinfo=timezone.utc),
        status="COMPLETED",
    )

    with pytest.raises(ValueError):
        rental.register_return(datetime(2026, 9, 15, 19, 30, tzinfo=timezone.utc))

    assert rental.return_time is None


def test_return_cannot_be_before_rental_start(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 14, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    with pytest.raises(ValueError):
        rental.register_return(datetime(2026, 9, 13, 17, 0, tzinfo=timezone.utc))

    assert rental.return_time is None


def test_rental_early_return(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 14, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 15, 15, 0, tzinfo=timezone.utc))

    assert rental.return_status == "EARLY"


def test_rental_on_time_return(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc))
    assert rental.return_status == "ON_TIME"


def test_rental_late_return(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 20, 18, 0, tzinfo=timezone.utc))
    assert rental.return_status == "LATE"


def test_cannot_register_return_twice(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    with pytest.raises(ValueError):
        assert rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))


def test_check_in_time(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    rental.check_in(
        check_in_time=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        odometer_in=8000,
        fuel_in=8,
        condition="NO_NEW_DAMAGE",
    )
    assert rental.check_in_time == (datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))


def test_odometer_in(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 15, 0, tzinfo=timezone.utc))
    rental.check_in(
        check_in_time=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        odometer_in=8000,
        fuel_in=8,
        condition="NO_NEW_DAMAGE",
    )
    assert rental.odometer_in == 8000


def test_fuel_in(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    rental.check_in(
        check_in_time=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        odometer_in=8000,
        fuel_in=8,
        condition="NO_NEW_DAMAGE",
    )
    assert rental.fuel_in == 8


def test_vehicle_condition(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    rental.check_in(
        check_in_time=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        odometer_in=8000,
        fuel_in=8,
        condition="NEW_DAMAGE",
    )
    assert rental.condition == "NEW_DAMAGE"


def test_check_in_success(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 16, 15, 20, tzinfo=timezone.utc),
        due=datetime(2026, 9, 17, 15, 20, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 17, 15, 20, tzinfo=timezone.utc))
    rental.check_in(
        check_in_time=datetime(2026, 9, 17, 15, 45, tzinfo=timezone.utc),
        odometer_in=8000,
        fuel_in=8,
        condition="NO_NEW_DAMAGE",
    )
    assert rental.check_in_status == "CHECKED-IN"
    assert rental.check_in_time == datetime(2026, 9, 17, 15, 45, tzinfo=timezone.utc)
    assert rental.odometer_in == 8000
    assert rental.fuel_in == 8
    assert rental.condition == "NO_NEW_DAMAGE"


def test_check_in_fails_when_vehicle_not_returned(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 16, 16, 30, tzinfo=timezone.utc),
        due=datetime(2026, 9, 17, 16, 30, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    with pytest.raises(ValueError):
        rental.check_in(
            check_in_time=datetime(2026, 9, 17, 16, 30, tzinfo=timezone.utc),
            odometer_in=8000,
            fuel_in=8,
            condition="NO_NEW_DAMAGE",
        )


def test_check_in_already_completed(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 21, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 21, 17, 0, tzinfo=timezone.utc))
    rental.check_in(
        check_in_time=datetime(2026, 9, 21, 17, 0, tzinfo=timezone.utc),
        odometer_in=8000,
        fuel_in=8,
        condition="NO_NEW_DAMAGE",
    )

    with pytest.raises(ValueError):
        rental.check_in(
            check_in_time=datetime(2026, 9, 30, 17, 0, tzinfo=timezone.utc),
            odometer_in=8000,
            fuel_in=8,
            condition="NO_NEW_DAMAGE",
        )


def test_check_in_cannot_be_earlier_than_return_time(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 21, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    with pytest.raises(ValueError):
        rental.register_return(datetime(2026, 9, 20, 18, 0, tzinfo=timezone.utc))
        rental.check_in(
            check_in_time=datetime(2026, 9, 20, 17, 30, tzinfo=timezone.utc),
            odometer_in=8000,
            fuel_in=8,
            condition="NO_NEW_DAMAGE",
        )


def test_check_in_odometer_cannot_be_lower_than_current(test_customer, test_vehicle):
    test_vehicle.odometer_km = 10000
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    with pytest.raises(ValueError):
        rental.check_in(
            check_in_time=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
            odometer_in=8000,
            fuel_in=8,
            condition="NO_NEW_DAMAGE",
        )

def test_rental_becomes_completed_when_vehicle_is_returned(test_customer, test_vehicle):
    rental = Rental(
         test_customer,
         test_vehicle,
         start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
         due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
         status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))

    assert rental.status == "COMPLETED"


def test_check_in_updates_current_odometer(test_customer, test_vehicle):
    rental = Rental(
        test_customer,
        test_vehicle,
        start=datetime(2026, 9, 15, 18, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE"
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    rental.check_in(check_in_time=datetime(2026, 9, 17, 17, 0, tzinfo=timezone.utc), odometer_in= 8500, fuel_in=8, condition="NO_NEW_DAMAGE")

    assert test_vehicle.odometer_km == 8500    