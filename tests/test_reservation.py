from datetime import datetime, timezone

import pytest

from app.models.customer import Customer
from app.models.reservation import Reservation
from app.models.vehicle import Vehicle, VehicleBlock
from app.services.rental_service import create_rental_from_reservation
from app.services.vehicle_service import assign_vehicle_to_reservation


# Test fixtures
@pytest.fixture
def test_customer():
    customer = Customer(
        customer_id="PA-5656",
        customer_type="PARTNER",
        first_name="Losugan",
        last_name="Sivasuthan",
        email="ssv1605@test.com",
        phone_number="+47 21390016",
    )

    return customer


@pytest.fixture
def test_vehicle():
    vehicle = Vehicle(
        registration_number="DS 35637",
        make="Volvo",
        model="XC-60",
        fuel_type="Petrol",
        operational_status="AVAILABLE",
        odometer_km=7500,
    )

    return vehicle


def test_reservation_rejects_end_before_start(test_customer, test_vehicle):

    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc)

    # create reservation
    with pytest.raises(ValueError):
        Reservation(
            customer=test_customer,
            vehicle=test_vehicle,
            start=start,
            end=end,
        )


def test_reservation_can_be_created_without_assigned_vehicle(test_customer):

    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 25, 20, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        test_customer,
        vehicle=None,
        start=start,
        end=end,
    )

    assert reservation.vehicle is None


def test_reservation_can_have_vehicle_after_creation(test_customer, test_vehicle):
    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 25, 20, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        test_customer,
        vehicle=None,
        start=start,
        end=end,
    )
    reservation.assign_vehicle(test_vehicle)

    assert reservation.vehicle is test_vehicle


def test_available_vehicle_can_be_assigned_to_reservation(test_customer, test_vehicle):
    reservation = Reservation(
        test_customer,
        None,
        start=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        end=datetime(2026, 9, 22, 17, 0, tzinfo=timezone.utc),
    )
    assign_vehicle_to_reservation(reservation, test_vehicle)

    assert reservation.vehicle == test_vehicle


def test_unavailable_vehicle_cannot_be_assigned_to_reservation(
    test_customer, test_vehicle
):
    reservation = Reservation(
        test_customer,
        None,
        start=datetime(2026, 9, 20, 17, 0, tzinfo=timezone.utc),
        end=datetime(2026, 9, 22, 17, 0, tzinfo=timezone.utc),
    )

    test_vehicle.add_block(
        VehicleBlock(
            block_type="MAINTENANCE",
            start=datetime(2026, 9, 21, 17, 0, tzinfo=timezone.utc),
            end=datetime(2026, 9, 23, 17, 0, tzinfo=timezone.utc),
            block_reason="Scheduled maintenance",
        )
    )

    with pytest.raises(
        ValueError, match="Vehicle is unavailable for the reservation period."
    ):
        assign_vehicle_to_reservation(reservation, test_vehicle)

    assert reservation.vehicle is None


def test_reservation_vehicle_can_be_reassigned(test_customer, test_vehicle):
    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 25, 20, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        test_customer,
        vehicle=test_vehicle,
        start=start,
        end=end,
    )

    new_vehicle = Vehicle(
        registration_number="ER 54777",
        make="AUDI",
        model="Q6 E-tron",
        fuel_type="Electric",
        operational_status="AVAILABLE",
        odometer_km=450,
    )
    reservation.assign_vehicle(new_vehicle)
    assert reservation.vehicle is new_vehicle


def test_reservation_vehicle_can_be_unassigned(test_customer, test_vehicle):
    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 25, 20, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        test_customer,
        vehicle=test_vehicle,
        start=start,
        end=end,
    )
    reservation.assign_vehicle(None)

    assert reservation.vehicle is None


def test_reservation_is_active(test_customer, test_vehicle):

    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 30, 17, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        customer=test_customer, vehicle=test_vehicle, start=start, end=end
    )

    assert reservation.is_active(datetime(2026, 9, 27, 12, 0, tzinfo=timezone.utc))


def test_reservation_is_not_active_before_start(test_customer, test_vehicle):

    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 30, 17, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        customer=test_customer, vehicle=test_vehicle, start=start, end=end
    )
    assert not reservation.is_active(datetime(2026, 9, 25, 16, 0, tzinfo=timezone.utc))


def test_reservation_is_not_active_after_rent(test_customer, test_vehicle):

    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 30, 17, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        customer=test_customer, vehicle=test_vehicle, start=start, end=end
    )

    assert not reservation.is_active(datetime(2026, 10, 1, 10, 0, tzinfo=timezone.utc))

    # testing boundary


def test_reservation_is_active_at_start(test_customer, test_vehicle):

    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 30, 17, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        customer=test_customer, vehicle=test_vehicle, start=start, end=end
    )

    assert reservation.is_active(start)


def test_reservation_can_be_converted_to_rental(test_customer, test_vehicle):
    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 30, 17, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        customer=test_customer,
        vehicle=test_vehicle,
        start=start,
        end=end,
    )

    rental = create_rental_from_reservation(reservation)

    assert rental.customer is reservation.customer
    assert rental.vehicle is reservation.vehicle
    assert rental.start == reservation.start
    assert rental.due == reservation.end
    assert rental.status == "ACTIVE"


def test_reservation_without_vehicle_cannot_create_rental(test_customer):
    start = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 25, 17, 0, tzinfo=timezone.utc)

    reservation = Reservation(
        customer=test_customer, vehicle=None, start=start, end=end
    )
    with pytest.raises(
        ValueError,
        match="The reservation must have an assigned vehicle before creating the Rental",
    ):
        create_rental_from_reservation(reservation)
