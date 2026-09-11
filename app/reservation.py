from datetime import datetime

from app.customer import Customer
from app.vehicle import Vehicle


class Reservation:
    def __init__(
        self, customer: Customer, vehicle: Vehicle, start: datetime, end: datetime
    ):
        self.customer = customer
        self.vehicle = vehicle
        self.start = start
        self.end = end


