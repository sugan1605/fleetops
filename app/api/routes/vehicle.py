from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.schemas.vehicle import VehicleResponse
from app.dependencies import get_vehicle_repository
from app.repositories.vehicle_repository import VehicleRepository

router = APIRouter()

@router.get("/vehicles", response_model=list[VehicleResponse])
def get_vehicles(
    repository: Annotated[ VehicleRepository, Depends(get_vehicle_repository),],
):
    return repository.get_all()


