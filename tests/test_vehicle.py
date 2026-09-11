from datetime import datetime
from app.vehicle import Vehicle, VehicleBlock


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
        start=datetime(2026, 9, 25, 13, 00),
        end=datetime(2026, 9, 29, 17, 00),
        block_reason="Customer reservation",
    )

    assert vehicle_block.block_type== "RESERVATION"
    assert vehicle_block.start == datetime(2026,9,25,13,00)
    assert vehicle_block.end == datetime(2026,9,29,17,00)
    assert vehicle_block.block_reason == "Customer reservation"