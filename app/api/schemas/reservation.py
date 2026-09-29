from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

## These are API schemas. They describe the data entering and leaving FastAPI

class ReservationResponse(BaseModel):
    reservation_id: UUID
    customer_id: str
    vehicle_id: UUID | None
    start: datetime
    end: datetime


class ReservationCreate(BaseModel):
    customer_id: str
    vehicle_id: UUID | None = None
    start: datetime
    end: datetime
    