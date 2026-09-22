from uuid import UUID

from app.database import get_connection
from app.models.vehicle import Vehicle

vehicle_id = UUID("46926fa9-ab15-42c4-9868-4d2a44b9d3ea")

with get_connection() as connection, connection.cursor() as cursor:
    cursor.execute(
        "SELECT * FROM vehicles WHERE vehicle_id = %s",
        (vehicle_id,)
    )

    result = cursor.fetchone()

    (
    vehicle_id,
    registration_number,
    make,
    model,
    fuel_type,
    operational_status,
    odometer_km,
    ) = result


vehicle = Vehicle(
    vehicle_id,
    registration_number,
    make,
    model,
    fuel_type,
    operational_status,
    odometer_km,
)

print(vehicle)
