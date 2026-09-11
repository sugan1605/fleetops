from datetime import datetime

from app.vehicle import Vehicle, VehicleBlock
from app.vehicle_service import get_available_vehicles


def test_vehicle_creation():
    vehicle = Vehicle(
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
        start=datetime(2026, 9, 25, 13, 0),
        end=datetime(2026, 9, 29, 17, 0),
        block_reason="Customer reservation",
    )

    assert vehicle_block.block_type == "RESERVATION"
    assert vehicle_block.start == datetime(2026, 9, 25, 13, 0)
    assert vehicle_block.end == datetime(2026, 9, 29, 17, 0)
    assert vehicle_block.block_reason == "Customer reservation"


def test_get_available_vehicles():
    # Arrange
    vehicle_1 = Vehicle(
        registration_number="SX 35685",
        make="Toyota",
        model="RAV 4",
        fuel_type="Petrol",
    )

    vehicle_2 = Vehicle(
        registration_number="DS 355542",
        make="Volvo",
        model="XC-90",
        fuel_type="Petrol",
    )

    vehicle_block = VehicleBlock(
        block_type="RESERVATION",
        start=datetime(2026, 9, 25, 13, 0),
        end=datetime(2026, 9, 29, 17, 0),
        block_reason="Customer reservation",
    )

    vehicle_2.add_block(vehicle_block)

    start = datetime(2026, 9, 26, 10, 0)
    end = datetime(2026, 9, 28, 10, 0)

    # Act
    available_vehicles = get_available_vehicles(
        [vehicle_1, vehicle_2],
        start,
        end,
    )

    # Assert
    assert available_vehicles == [vehicle_1]
