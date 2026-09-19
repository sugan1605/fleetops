from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.models.customer import Customer
from app.models.rental import Rental
from app.models.reservation import Reservation
from app.models.vehicle import Vehicle, VehicleBlock
from app.services.rental_service import extend_rental, validate_rental_overlap


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
def vehicle():
    return Vehicle(
        vehicle_id=uuid4(),
        registration_number="SX 503335",
        make="Volvo",
        model="XC-60",
        fuel_type="Petrol",
        odometer_km=8000,
    )


def test_rental_can_be_created(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 17, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    assert rental.customer is test_customer
    assert rental.vehicle is vehicle
    assert rental.start == datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc)
    assert rental.due == datetime(2026, 9, 17, 17, 0, tzinfo=timezone.utc)
    assert rental.status == "ACTIVE"


def test_rental_invalid_status(test_customer, vehicle):
    with pytest.raises(ValueError):
        Rental(
            test_customer,
            vehicle,
            start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
            due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
            status="INVALID",
        )


def test_new_rental_has_not_returned_status(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 17, 14, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 18, 14, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    assert rental.return_status == "NOT_RETURNED"


def test_rental_due_date_cannot_be_before_start_date(test_customer, vehicle):
    with pytest.raises(ValueError):
        Rental(
            test_customer,
            vehicle,
            start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
            due=datetime(2026, 9, 14, 17, 0, tzinfo=timezone.utc),
            status="ACTIVE",
        )


def test_active_rental_can_register_return(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 14, 21, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 15, 21, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    rental.register_return(datetime(2026, 9, 15, 19, 30, tzinfo=timezone.utc))

    assert rental.return_time == datetime(2026, 9, 15, 19, 30, tzinfo=timezone.utc)


def test_non_active_rental_cannot_register_return(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 14, 21, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 15, 21, 0, tzinfo=timezone.utc),
        status="COMPLETED",
    )

    with pytest.raises(ValueError):
        rental.register_return(datetime(2026, 9, 15, 19, 30, tzinfo=timezone.utc))


def test_return_cannot_be_before_rental_start(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 14, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    with pytest.raises(ValueError):
        rental.register_return(datetime(2026, 9, 13, 17, 0, tzinfo=timezone.utc))

    assert rental.return_time is None


def test_rental_early_return(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 14, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 15, 15, 0, tzinfo=timezone.utc))

    assert rental.return_status == "EARLY"


def test_rental_on_time_return(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc))
    assert rental.return_status == "ON_TIME"


def test_rental_late_return(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 20, 18, 0, tzinfo=timezone.utc))
    assert rental.return_status == "LATE"


def test_cannot_register_return_twice(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    with pytest.raises(ValueError):
        assert rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))


def test_check_in_time(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
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


def test_odometer_in(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
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


def test_fuel_in(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
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


def test_vehicle_condition(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
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


def test_check_in_success(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
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


def test_check_in_fails_when_vehicle_not_returned(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
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


def test_active_rantal_can_be_extended_when_vehicle_is_available(
    test_customer, vehicle
):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 17, 15, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 19, 15, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.extend(new_due=datetime(2026, 9, 20, 15, 0, tzinfo=timezone.utc))
    assert rental.due == datetime(2026, 9, 20, 15, 0, tzinfo=timezone.utc)


def test_rental_extension_is_rejected_when_vehicle_has_conflicting_reservation(
    test_customer,
    vehicle,
):
    rental_extension = datetime(2026, 9, 20, 15, 0, tzinfo=timezone.utc)

    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 17, 15, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 19, 16, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    reservation = Reservation(
        customer=test_customer,
        vehicle=vehicle,
        start=datetime(2026, 9, 20, 14, 30, tzinfo=timezone.utc),
        end=datetime(2026, 9, 23, 15, 0, tzinfo=timezone.utc),
    )

    with pytest.raises(ValueError):
        extend_rental(rental, rental_extension, [reservation])


def test_rental_extention_is_allowed_when_no_reservation_conflicts(
    test_customer, vehicle
):
    rental_extension = datetime(2026, 9, 24, 15, 0, tzinfo=timezone.utc)

    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 20, 14, 30, tzinfo=timezone.utc),
        due=datetime(2026, 9, 21, 14, 30, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    reservation = Reservation(
        customer=test_customer,
        vehicle=vehicle,
        start=datetime(2026, 9, 25, 14, 30, tzinfo=timezone.utc),
        end=datetime(2026, 9, 30, 14, 30, tzinfo=timezone.utc),
    )
    extend_rental(rental, rental_extension, [reservation])

    assert rental.due == rental_extension


def test_check_in_already_completed(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
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


def test_check_in_cannot_be_earlier_than_return_time(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 21, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 20, 18, 0, tzinfo=timezone.utc))
    with pytest.raises(ValueError):
        rental.check_in(
            check_in_time=datetime(2026, 9, 20, 17, 30, tzinfo=timezone.utc),
            odometer_in=8000,
            fuel_in=8,
            condition="NO_NEW_DAMAGE",
        )


def test_check_in_odometer_cannot_be_lower_than_current(test_customer, vehicle):
    vehicle.odometer_km = 10000
    rental = Rental(
        test_customer,
        vehicle,
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


def test_rental_becomes_completed_when_vehicle_is_returned(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))

    assert rental.status == "COMPLETED"


def test_rental_extension_cannot_shorten_rental(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    with pytest.raises(ValueError):
        extend_rental(rental, datetime(2026, 9, 16, 0, tzinfo=timezone.utc), [])


def test_rental_completed_rental_cannot_extend_rental(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="COMPLETED",
    )
    with pytest.raises(ValueError):
        extend_rental(rental, datetime(2026, 9, 17, 17, 0, tzinfo=timezone.utc), [])


def test_rental_cannot_be_extended_if_car_blocked_for_service_or_sale(
    test_customer, vehicle
):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )

    service_block = VehicleBlock(
        block_type="MAINTENANCE",
        start=datetime(2026, 9, 17, 17, 0, tzinfo=timezone.utc),
        end=datetime(2026, 9, 19, 17, 0, tzinfo=timezone.utc),
        block_reason="Yearly Service",
    )

    vehicle.add_block(service_block)

    with pytest.raises(ValueError):
        extend_rental(rental, datetime(2026, 9, 18, 15, 0, tzinfo=timezone.utc), [])

    assert rental.due == datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc)


def test_same_vehicle_cannot_have_overlapping_rentals(test_customer, vehicle):
    rental_one = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 18, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental_two = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 17, 12, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    with pytest.raises(ValueError):
        validate_rental_overlap(
            rental_two,
            [rental_one],
        )


def test_check_in_updates_current_odometer(test_customer, vehicle):
    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 18, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    rental.check_in(
        check_in_time=datetime(2026, 9, 17, 17, 0, tzinfo=timezone.utc),
        odometer_in=8500,
        fuel_in=8,
        condition="NO_NEW_DAMAGE",
    )

    assert vehicle.odometer_km == 8500


def test_check_in_marks_vehicle_as_dirty(test_customer, vehicle):
    vehicle.operational_status = "ON_A_RENT"
    vehicle.odometer_km = 8000

    rental = Rental(
        test_customer,
        vehicle,
        start=datetime(2026, 9, 15, 18, 0, tzinfo=timezone.utc),
        due=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        status="ACTIVE",
    )
    rental.register_return(datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc))
    rental.check_in(
        check_in_time=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
        odometer_in=8500,
        fuel_in=8,
        condition="NO_NEW_DAMAGE",
    )

    assert vehicle.operational_status == "DIRTY"
