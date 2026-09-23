from uuid import UUID

from pydantic import BaseModel


class ReservationResponse(BaseModel):
    reservation_id : UUID
    