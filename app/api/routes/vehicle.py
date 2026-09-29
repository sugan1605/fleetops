from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.vehicle import VehicleResponse
from app.dependencies import get_vehicle_repository
from app.repositories.vehicle_repository import VehicleRepository

router = APIRouter()

@router.get("/vehicles", response_model=list[VehicleResponse])
def get_vehicles(
    repository: Annotated[ VehicleRepository, Depends(get_vehicle_repository),],
):
    return repository.get_all()

@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
def get_vehicle_by_id(vehicle_id: UUID, repository: Annotated[VehicleRepository, Depends(get_vehicle_repository),],):
    vehicle = repository.get_by_id(vehicle_id)

    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )

    return vehicle



