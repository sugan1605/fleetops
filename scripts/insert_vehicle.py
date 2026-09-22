from uuid import uuid4

from app.database import get_connection

vehicle_id = uuid4()

with get_connection() as connection, connection.cursor() as cursor:
    cursor.execute(
        "INSERT INTO vehicles(vehicle_id, registration_number, make, model, fuel_type, operational_status, odometer_km)"
        "VALUES (%s,%s,%s,%s,%s,%s,%s)",
        (vehicle_id,
         "EA 18743",
         "BMW",
         "IX3 M50",
         "Electric",
         "AVAILABLE",
         2600,
         ),
        )