from datetime import datetime, timezone
from uuid import uuid4

import pytest

from app.models.vehicle import Vehicle, VehicleBlock
from app.services.vehicle_service import get_available_vehicles


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

@pytest.fixture
def maintenance_block():
    return VehicleBlock(
        block_type="MAINTENANCE",
        start=datetime(2026, 9, 15, 18, 0, tzinfo=timezone.utc),
        end=datetime(2026, 9, 17, 18, 0, tzinfo=timezone.utc),
        block_reason="Tire change"
    )


def test_vehicle_creation():
    vehicle = Vehicle(
        vehicle_id=uuid4(),
        registration_number="DS 35467",
        make="Volvo",
        model="XC60",
        fuel_type="Petrol",
        odometer_km=25000,
        operational_status="AVAILABLE",
    )

    assert vehicle.registration_number == "DS 35467"
    assert vehicle.make == "Volvo"
    assert vehicle.model == "XC60"
    assert vehicle.fuel_type == "Petrol"
    assert vehicle.odometer_km == 25000
    assert vehicle.operational_status == "AVAILABLE"


def test_vehicle_block():
    vehicle_block = VehicleBlock(
        block_type="RESERVATION",
        start=datetime(2026, 9, 25, 13, 0, tzinfo=timezone.utc),
        end=datetime(2026, 9, 29, 17, 0, tzinfo=timezone.utc),
        block_reason="Customer reservation",
    )

    assert vehicle_block.block_type == "RESERVATION"
    assert vehicle_block.start == datetime(2026, 9, 25, 13, 0, tzinfo=timezone.utc)
    assert vehicle_block.end == datetime(2026, 9, 29, 17, 0, tzinfo=timezone.utc)
    assert vehicle_block.block_reason == "Customer reservation"


def test_dirty_vehicle_is_not_available(vehicle):
    vehicle.operational_status = "DIRTY"

    assert (
    vehicle.is_available(
    start=datetime(2026, 9, 15, 17, 0, tzinfo=timezone.utc),
    end=datetime(2026, 9, 16, 17, 0, tzinfo=timezone.utc),
    )
        is False
    )

def test_vehicle_with_maintenance_block_is_not_available(vehicle, maintenance_block):
    vehicle.add_block(maintenance_block)

    assert vehicle.is_available(start=datetime(2026, 9, 14, 17, 0, tzinfo=timezone.utc), end=datetime(2026, 9, 17, 16, 30, tzinfo=timezone.utc)) is False


def test_vehicle_can_be_marked_available_after_cleaning(vehicle):
    vehicle.operational_status = "DIRTY"
    vehicle.mark_ready()
    assert vehicle.operational_status == "AVAILABLE"


def test_get_available_vehicles():
    # Arrange
    vehicle_1 = Vehicle(
        vehicle_id=uuid4(),
        registration_number="SX 35685",
        make="Toyota",
        model="RAV 4",
        fuel_type="Petrol",
    )

    vehicle_2 = Vehicle(
        vehicle_id=uuid4(),
        registration_number="DS 355542",
        make="Volvo",
        model="XC-90",
        fuel_type="Petrol",
    )

    vehicle_block = VehicleBlock(
        block_type="RESERVATION",
        start=datetime(2026, 9, 25, 13, 0, tzinfo=timezone.utc),
        end=datetime(2026, 9, 29, 17, 0, tzinfo=timezone.utc),
        block_reason="Customer reservation",
    )

    vehicle_2.add_block(vehicle_block)

    start = datetime(2026, 9, 26, 10, 0, tzinfo=timezone.utc)
    end = datetime(2026, 9, 28, 10, 0, tzinfo=timezone.utc)

    # Act
    available_vehicles = get_available_vehicles(
        [vehicle_1, vehicle_2],
        start,
        end,
    )

    # Assert
    assert available_vehicles == [vehicle_1]



