from uuid import uuid4

from app.models.vehicle import Vehicle
from app.repositories.vehicle_repository import VehicleRepository

vehicle_repository = VehicleRepository()

def get_vehicle_repository():
    return vehicle_repository


vehicle = Vehicle(
    vehicle_id=uuid4(),
    registration_number="EA 18743",
    make="BMW",
    model="IX3",
    fuel_type="Electric",
    odometer_km=2600
)

vehicle_repository.add(vehicle)