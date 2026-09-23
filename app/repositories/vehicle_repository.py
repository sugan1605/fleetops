from uuid import UUID

from app.database import get_connection
from app.models.vehicle import Vehicle


class VehicleRepository:
    def _row_to_vehicle(self, row) -> Vehicle:
        (
            vehicle_id,
            registration_number,
            make,
            model,
            fuel_type,
            operational_status,
            odometer_km,
        ) = row

        return Vehicle(
            vehicle_id,
            registration_number,
            make,
            model,
            fuel_type,
            operational_status,
            odometer_km,
        )

    def add(self, vehicle: Vehicle):
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO vehicles"
                "(vehicle_id, registration_number, make, model, fuel_type, "
                "operational_status, odometer_km)"
                "VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (
                    vehicle.vehicle_id,
                    vehicle.registration_number,
                    vehicle.make,
                    vehicle.model,
                    vehicle.fuel_type,
                    vehicle.operational_status,
                    vehicle.odometer_km,
                ),
            )

    def get_all(self) -> list[Vehicle]:
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM vehicles")

            results = cursor.fetchall()

            vehicles = []

            for result in results:
                vehicles.append(self._row_to_vehicle(result))

        return vehicles

    def get_by_id(self, vehicle_id: UUID) -> Vehicle | None:
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM vehicles WHERE vehicle_id = %s", (vehicle_id,)
            )

            result = cursor.fetchone()

            if not result:
                return None

        return self._row_to_vehicle(result)

    def delete(self, vehicle_id: UUID) -> None:
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM vehicles WHERE vehicle_id = %s",
                (vehicle_id,),
            )
