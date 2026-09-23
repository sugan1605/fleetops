from uuid import uuid4

from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository


def create_vehicle(registration_number: str = 'EA 18743'):
    return Vehicle(
        vehicle_id=uuid4(),
        registration_number=registration_number,
        make="BMW",
        model="IX3 M50",
        fuel_type="Electric",
        odometer_km=2600,
    )





def test_add_vehicle_and_get_all():
    repository = VehicleRepository()
    vehicle = create_vehicle("EA 18743")

    repository.add(vehicle)
    vehicles = repository.get_all()

    assert vehicles == [vehicle]


def test_get_vehicle_by_id():
    repository = VehicleRepository()
    vehicle = create_vehicle("EJ 24561")
    repository.add(vehicle)

    result = repository.get_by_id(vehicle.vehicle_id)

    assert result == vehicle


def test_get_vehicle_by_id_returns_none_when_not_found():
    repository = VehicleRepository()
    vehicle = create_vehicle("ER 38192")
    repository.add(vehicle)

    result = repository.get_by_id(uuid4())

    assert result is None 
      
