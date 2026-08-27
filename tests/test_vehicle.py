from app.vehicle import Vehicle

def test_vehicle_creation():
    vehicle = Vehicle (
        registration_number= "DS 35467",
        make= "Volvo",
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