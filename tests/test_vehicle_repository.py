from uuid import uuid4

import pytest

from app.database import get_connection
from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository


@pytest.fixture
def repository(monkeypatch):
    monkeypatch.setenv("FLEETOPS_DB_NAME", "fleetops_test")
    repository = VehicleRepository()
    yield repository

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM vehicles")


def create_vehicle(registration_number: str = "EA 18743"):
    return Vehicle(
        vehicle_id=uuid4(),
        registration_number=registration_number,
        make="BMW",
        model="IX3 M50",
        fuel_type="Electric",
        odometer_km=2600,
    )


def test_add_vehicle_and_get_all(repository):
    vehicle = create_vehicle("EA 18743")

    repository.add(vehicle)
    vehicles = repository.get_all()

    assert vehicles == [vehicle]


def test_get_vehicle_by_id(repository):
    vehicle = create_vehicle("EJ 24561")
    repository.add(vehicle)

    result = repository.get_by_id(vehicle.vehicle_id)

    assert result == vehicle


def test_get_vehicle_by_id_returns_none_when_not_found(repository):

    result = repository.get_by_id(uuid4())

    assert result is None


def test_delete_vehicle(repository):

    vehicle = create_vehicle("EJ 77781")

    repository.add(vehicle)
    repository.delete(vehicle.vehicle_id)

    result = repository.get_by_id(vehicle.vehicle_id)

    assert result is None
