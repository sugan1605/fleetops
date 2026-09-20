## In-memory list before I create database
from uuid import UUID

from app.models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self):
        self.vehicles: dict[UUID, Vehicle] = {}

    def add(self, vehicle: Vehicle):
        self.vehicles[vehicle.vehicle_id] = vehicle

    def get_all(self) -> list[Vehicle]:
        return list(self.vehicles.values())

    def get_by_id(self, vehicle_id: UUID) -> Vehicle | None:
        return self.vehicles.get(vehicle_id)
