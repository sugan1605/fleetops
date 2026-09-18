from datetime import datetime

from app.models.reservation import Reservation
from app.models.vehicle import Vehicle


def get_available_vehicles(
    vehicles: list[Vehicle], start: datetime, end: datetime
) -> list[Vehicle]:
    available_vehicles = []

    for vehicle in vehicles:
        if vehicle.is_available(start, end):
            available_vehicles.append(vehicle)

    return available_vehicles


def assign_vehicle_to_reservation(reservation: Reservation, vehicle: Vehicle):
    if not vehicle.is_available(reservation.start, reservation.end):
        raise ValueError("Vehicle is unavailable for the reservation period.")
    reservation.assign_vehicle(vehicle)
