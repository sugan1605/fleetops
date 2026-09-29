from uuid import UUID

from pydantic import BaseModel


class VehicleResponse(BaseModel):
    vehicle_id: UUID
    registration_number: str
    make: str
    model: str
    fuel_type: str
    operational_status: str
    odometer_km: int