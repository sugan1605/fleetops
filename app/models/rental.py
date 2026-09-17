from datetime import datetime

from app.models.customer import Customer
from app.models.vehicle import Vehicle


class Rental:
    # Rental state is represented through separate status dimensions.
    # This allows the rental, return, check-in and vehicle condition
    # process to progress independently.
    VALID_STATUSES = (
        "ACTIVE",
        "COMPLETED",
        "CANCELLED",
        "VOIDED",
    )

    RETURN_STATUSES = (
        "NOT_RETURNED",
        "EARLY",
        "ON_TIME",
        "LATE",
    )

    CHECK_IN_STATUSES = (
        "PENDING",
        "CHECKED-IN",
        "FINALIZED",
    )

    CONDITION_STATUSES = (
        "NO_NEW_DAMAGE",
        "NEW_DAMAGE",
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
            raise ValueError("Due date can't be earlier than start date.")

        self.customer = customer
        self.vehicle = vehicle
        self.start = start
        self.due = due
        self.status = status
        self.return_time = None
        self.check_in_time = None
        self.odometer_in = None
        self.fuel_in = None
        self.condition = None
        self.check_in_status = "PENDING"

    def register_return(self, return_time: datetime):
        # Customer-facing event: records when the vehicle was returned.
        # The rental is completed at this point, even though employee
        # inspection may happen later.

        if self.status != "ACTIVE":
            raise ValueError("Only active rental can register a return.")

        if self.return_time is not None:
            raise ValueError("The return has already been registered.")

        if return_time < self.start:
            raise ValueError("Return time can't be earlier than start time")

        self.return_time = return_time

        if return_time < self.due:
            self.return_status = "EARLY"

        elif return_time == self.due:
            self.return_status = "ON_TIME"

        else:
            self.return_status = "LATE"

        self.status = "COMPLETED"

    def check_in(
        self, check_in_time: datetime, odometer_in: int, fuel_in: int, condition: str
    ):
        # Operational event: an employee physically checks the returned
        # vehicle and records its condition, milage and fuel level.

        if self.return_time is None:
            raise ValueError("The car hasn't been returned. The check-in has to wait.")

        if self.check_in_status == "CHECKED-IN":
            raise ValueError("The car is already checked in.")

        if check_in_time < self.return_time:
            raise ValueError("Check-in time cannot be earlier than return time.")

        if odometer_in < self.vehicle.odometer_km:
            raise ValueError("The in km can't be lower than current km.")

        if condition not in self.CONDITION_STATUSES:
            raise ValueError("invalid condition entered")

        self.vehicle.odometer_km = odometer_in

        # Once the employee has completed the physical check-in,
        # the vehicle is marked DIRTY because it still needs cleaning
        # before it can become available for the next rental.
        self.vehicle.update_operational_status("DIRTY")

        self.check_in_time = check_in_time
        self.odometer_in = odometer_in
        self.fuel_in = fuel_in
        self.condition = condition
        self.check_in_status = "CHECKED-IN"
