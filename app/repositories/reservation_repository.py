from uuid import UUID

from app.database import get_connection
from app.models.reservation import Reservation
from app.repositories.customer_repository import CustomerRepository
from app.repositories.vehicle_repository import VehicleRepository


class ReservationRepository:
    def __init__(
        self,
        customer_repository=CustomerRepository,
        vehicle_repository=VehicleRepository,
    ):
        self.customer_repository = customer_repository
        self.vehicle_repository = vehicle_repository

    def _row_to_reservation(self, row) -> Reservation:
        (
            reservation_id,
            customer_id,
            vehicle_id,
            start_at,
            end_at,
        ) = row

        customer = self.customer_repository.get_by_id(customer_id)

        vehicle = None
        if vehicle_id is not None:
            vehicle = self.vehicle_repository.get_by_id(vehicle_id)

        return Reservation(reservation_id, customer, vehicle, start_at, end_at)

    def add(self, reservation: Reservation):

        vehicle_id = (
            reservation.vehicle.vehicle_id if reservation.vehicle is not None else None
        )
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO reservations"
                "(reservation_id, customer_id, vehicle_id, start_at, end_at)"
                "VALUES(%s, %s, %s, %s, %s)",
                (
                    reservation.reservation_id,
                    reservation.customer.customer_id,
                    vehicle_id,
                    reservation.start,
                    reservation.end,
                ),
            )

    def get_by_id(self, reservation_id: UUID) -> Reservation | None:
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM reservations WHERE reservation_id = %s",
                (reservation_id,),
            )

            result = cursor.fetchone()

            if result is None:
                return None

            return self._row_to_reservation(result)
