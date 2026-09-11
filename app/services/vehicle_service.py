from datetime import datetime

from app.models.vehicle import Vehicle

def get_available_vehicles(
    vehicles: list[Vehicle],
    start: datetime,
    end: datetime
    ) -> list[Vehicle]:
    available_vehicles = []

    for vehicle in vehicles:
        if vehicle.is_available(start, end):
            available_vehicles.append(vehicle)


    return available_vehicles