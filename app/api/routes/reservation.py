from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.reservation import ReservationCreate, ReservationResponse
from app.dependencies import (
    get_customer_repository,
    get_reservation_repository,
    get_vehicle_repository,
)
from app.models.reservation import Reservation
from app.repositories.customer_repository import CustomerRepository
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.vehicle_repository import VehicleRepository

router = APIRouter()


@router.post(
    "/reservations",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reservation(
    reservation_data: ReservationCreate,
    customer_repository: Annotated[
        CustomerRepository, Depends(get_customer_repository)
    ],
    vehicle_repository: Annotated[VehicleRepository, Depends(get_vehicle_repository)],
    reservation_repository: Annotated[
        ReservationRepository, Depends(get_reservation_repository)
    ],
):

    customer = customer_repository.get_by_id(reservation_data.customer_id)

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    vehicle = None

    if reservation_data.vehicle_id is not None:
        vehicle = vehicle_repository.get_by_id(reservation_data.vehicle_id)

        if vehicle is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found",
            )

    reservation = Reservation(
        reservation_id=uuid4(),
        customer=customer,
        vehicle=vehicle,
        start=reservation_data.start,
        end=reservation_data.end,
    )

    reservation_repository.add(reservation)

    return ReservationResponse(
        reservation_id=reservation.reservation_id,
        customer_id=reservation.customer.customer_id,
        vehicle_id=(
            reservation.vehicle.vehicle_id if reservation.vehicle is not None else None
        ),
        start=reservation.start,
        end=reservation.end,
    )


@router.get(
    "/reservations/{reservation_id}",
    response_model=ReservationResponse,
)
def get_reservation(
    reservation_id: UUID,
    reservation_repository: Annotated[
        ReservationRepository, Depends(get_reservation_repository)
    ],
):
    reservation = reservation_repository.get_by_id(reservation_id)

    if reservation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )

    return ReservationResponse(
        reservation_id=reservation_id,
        customer_id=reservation.customer.customer_id,
        vehicle_id=(
            reservation.vehicle.vehicle_id if reservation.vehicle is not None else None
        ),
        start=reservation.start,
        end=reservation.end,
    )
