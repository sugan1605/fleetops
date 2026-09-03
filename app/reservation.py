from datetime import datetime

from app.customer import Customer
from app.vehicle import Vehicle


class Reservation:
    def __init__(
        self, customer: Customer, vehicle: Vehicle, start: datetime, end: datetime
    ):
        if end < start:
            raise ValueError("end date can't be earlier than start date.")
        
        self.customer = customer
        self.vehicle = vehicle
        self.start = start
        self.end = end

    def is_active(self, current_time: datetime) -> bool:
        return self.start <= current_time <= self.end


    



    