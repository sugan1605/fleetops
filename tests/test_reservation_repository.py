from datetime import UTC, datetime
from uuid import uuid4

import pytest

from app.database import get_connection
from app.models.customer import Customer
from app.models.reservation import Reservation
from app.models.vehicle import Vehicle
from app.repositories.customer_repository import CustomerRepository
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.vehicle_repository import VehicleRepository


@pytest.fixture
def repository(monkeypatch):
    monkeypatch.setenv("FLEETOPS_DB_NAME", "fleetops_test")

    customer_repository = CustomerRepository()
    vehicle_repository = VehicleRepository()

    repository = ReservationRepository(
        customer_repository=customer_repository,
        vehicle_repository=vehicle_repository,
    )

    yield repository

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM reservations")
        cursor.execute("DELETE FROM vehicles")
        cursor.execute("DELETE FROM customers")


## test data


def create_customer():
    return Customer(
        customer_id="PA-5054",
        customer_type="PARTNER",
        first_name="Test",
        last_name="Customer",
        email="reservation@test.no",
        phone_number="+4712345678",
    )


def create_vehicle():
    return Vehicle(
        vehicle_id=uuid4(),
        registration_number="EA 18743",
        make="BMW",
        model="IX3 M50",
        fuel_type="Electric",
        odometer_km=2600,
    )


def test_add_reservation_and_get_by_id(repository):
    customer = create_customer()
    vehicle = create_vehicle()

    repository.customer_repository.add(customer)
    repository.vehicle_repository.add(vehicle)

    reservation = Reservation(
        reservation_id=uuid4(),
        customer=customer,
        vehicle=vehicle,
        start=datetime(2026, 10, 1, 10, 0, tzinfo=UTC),
        end=datetime(2026, 10, 5, 10, 0, tzinfo=UTC),
    )

    repository.add(reservation)

    result = repository.get_by_id(reservation.reservation_id)

    assert result is not None
    assert result.reservation_id == reservation.reservation_id
    assert result.customer == customer
    assert result.vehicle == vehicle
    assert result.start == reservation.start
    assert result.end == reservation.end


def test_add_reservation_without_vehicle_and_get_by_id(repository):
    customer = create_customer()

    repository.customer_repository.add(customer)

    reservation = Reservation(
        reservation_id=uuid4(),
        customer=customer,
        vehicle=None,
        start=datetime(2026, 10, 1, 10, 0, tzinfo=UTC),
        end=datetime(2026, 10, 5, 10, 0, tzinfo=UTC),
    )

    repository.add(reservation)

    result = repository.get_by_id(reservation.reservation_id)

    assert result is not None
    assert result.reservation_id == reservation.reservation_id
    assert result.customer == customer
    assert result.vehicle is None
    assert result.start == reservation.start
    assert result.end == reservation.end


def test_get_reservation_by_id_returns_none_when_not_found(repository):
    result = repository.get_by_id(uuid4())

    assert result is None