from datetime import datetime

from app.models.rental import Rental
from app.models.reservation import Reservation

# Can this rental's new end time coexist
# with existing reservation for this vehicle?


def extend_rental(rental: Rental, new_due: datetime, reservations: list[Reservation]):
    for reservation in reservations:
        if (
            reservation.vehicle == rental.vehicle
            and rental.due < reservation.end
            and new_due > reservation.start
        ):
            raise ValueError("Rental extension conflicts with an existing reservation.")

    if rental.vehicle.is_blocked_during(rental.due, new_due):
        raise ValueError("Rental extension conflicts with a vehicle block.") 
       
    rental.extend(new_due)


def validate_rental_overlap(rental: Rental, existing_rentals: list[Rental],):
    for existing_rental in existing_rentals:
        if(
            existing_rental.vehicle == rental.vehicle
            and rental.start < existing_rental.due
            and rental.due > existing_rental.start
        ):
            raise ValueError("Rental conflicts with an existing rental.")    
