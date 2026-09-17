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
    rental.extend(new_due)
