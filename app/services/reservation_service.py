from app.models.reservation import Reservation
from app.models.vehicle import Vehicle


def assign_vehicle_to_reservation(reservation: Reservation, vehicle: Vehicle):
    if not vehicle.is_available(reservation.start, reservation.end):
        raise ValueError("Vehicle is unavailable for the reservation period.")
    reservation.assign_vehicle(vehicle)