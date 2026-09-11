from datetime import datetime

from app.customer import Customer
from app.vehicle import Vehicle


class Rental:
    VALID_STATUSES = (
        "ACTIVE",
        "COMPLETED",
        "CANCELLED",
        "VOIDED",
    )

    def __init__(
        self,
        customer: Customer,
        vehicle: Vehicle,
        start: datetime,
        due: datetime,
        status: str,
    ):

        if status not in self.VALID_STATUSES:
            raise ValueError("Invalid status, please check status.")

        if due < start:
            raise ValueError("Due date can't be earlier than start date")

        self.customer = customer
        self.vehicle = vehicle
        self.start = start
        self.due = due
        self.status = status
