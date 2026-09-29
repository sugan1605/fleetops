from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from app.models.customer import Customer
from app.models.vehicle import Vehicle


class Reservation:
    def __init__(
        self,
        reservation_id: UUID,
        customer: Customer,
        vehicle: Optional[Vehicle],
        start: datetime,
        end: datetime,
    ):
        if end < start:
            raise ValueError("end date can't be earlier than start date.")
        self.reservation_id = reservation_id
        self.customer = customer
        self.vehicle = vehicle
        self.start = start
        self.end = end

    def is_active(self, current_time: datetime) -> bool:
        return self.start <= current_time <= self.end

    def assign_vehicle(self, vehicle: Optional[Vehicle]):
        self.vehicle = vehicle

 
    