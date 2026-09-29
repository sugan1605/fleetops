from datetime import UTC, datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.database import get_connection
from app.main import app
from app.models.customer import Customer
from app.models.vehicle import Vehicle
from app.repositories.customer_repository import CustomerRepository
from app.repositories.vehicle_repository import VehicleRepository

client = TestClient(app)


@pytest.fixture
def test_database(monkeypatch):
    monkeypatch.setenv("FLEETOPS_DB_NAME", "fleetops_test")

    customer_repository = CustomerRepository()
    vehicle_repository = VehicleRepository()

    customer = Customer(
        customer_id="PA-5054",
        customer_type="PARTNER",
        first_name="Test",
        last_name="Customer",
        email="api-reservation@test.no",
        phone_number="+4712345678",
    )

    vehicle = Vehicle(
        vehicle_id=uuid4(),
        registration_number="ER 54321",
        make="BMW",
        model="IX1",
        fuel_type="Electric",
        odometer_km=2600,
    )

    customer_repository.add(customer)
    vehicle_repository.add(vehicle)

    yield customer, vehicle

    with get_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DELETE FROM reservations")
        cursor.execute("DELETE FROM vehicles")
        cursor.execute("DELETE FROM customers")


def test_create_reservation(test_database):
    customer, vehicle = test_database

    response = client.post(
        "/reservations",
        json={
            "customer_id": customer.customer_id,
            "vehicle_id": str(vehicle.vehicle_id),
            "start": datetime(2026, 10, 1, 10, 0, tzinfo=UTC).isoformat(),
            "end": datetime(2026, 10, 5, 10, 0, tzinfo=UTC).isoformat(),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_id"] == customer.customer_id
    assert data["vehicle_id"] == str(vehicle.vehicle_id)
    assert data["start"] == "2026-10-01T10:00:00Z"
    assert data["end"] == "2026-10-05T10:00:00Z"
    assert "reservation_id" in data


def test_create_reservation_customer_not_found(test_database):
    _, vehicle = test_database

    response = client.post(
        "/reservations",
        json={
            "customer_id": "UNKNOWN-123",
            "vehicle_id": str(vehicle.vehicle_id),
            "start": datetime(2026, 10, 1, 10, 0, tzinfo=UTC).isoformat(),
            "end": datetime(2026, 10, 5, 10, 0, tzinfo=UTC).isoformat(),
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Customer not found"


def test_create_reservation_vehicle_not_found(test_database):
    customer, _ = test_database

    response = client.post(
        "/reservations",
        json={
            "customer_id": customer.customer_id,
            "vehicle_id": str(uuid4()),
            "start": datetime(2026, 10, 1, 10, 0, tzinfo=UTC).isoformat(),
            "end": datetime(2026, 10, 5, 10, 0, tzinfo=UTC).isoformat(),
        },
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Vehicle not found"


def test_create_reservation_without_vehicle(test_database):
    customer, _ = test_database

    response = client.post(
        "/reservations",
        json={
            "customer_id": customer.customer_id,
            "vehicle_id": None,
            "start": datetime(2026, 10, 1, 10, 0, tzinfo=UTC).isoformat(),
            "end": datetime(2026, 10, 5, 10, 0, tzinfo=UTC).isoformat(),
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_id"] == customer.customer_id
    assert data["vehicle_id"] is None
    assert data["start"] == "2026-10-01T10:00:00Z"
    assert data["end"] == "2026-10-05T10:00:00Z"
    assert "reservation_id" in data


def test_get_reservation(test_database):
    customer, vehicle = test_database

    start = datetime(2026, 10, 1, 10, 0, tzinfo=UTC)
    end = datetime(2026, 10, 5, 10, 0, tzinfo=UTC)

    create_response = client.post(
        "/reservations",
        json={
            "customer_id": customer.customer_id,
            "vehicle_id": str(vehicle.vehicle_id),
            "start" : start.isoformat(),
            "end" : end.isoformat()
        },
    )

    assert create_response.status_code == 201

    reservation_id = create_response.json()["reservation_id"]

    response = client.get(f"/reservations/{reservation_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["reservation_id"] == reservation_id
    assert data["customer_id"] == customer.customer_id
    assert data["vehicle_id"] == str(vehicle.vehicle_id)
    assert datetime.fromisoformat(data["start"]) == start
    assert datetime.fromisoformat(data["end"]) == end


def test_get_reservation_not_found():
    reservation_id = uuid4()

    response = client.get(f"/reservations/{reservation_id}")

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Reservation not found"
