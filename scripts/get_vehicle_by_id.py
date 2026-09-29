from app.database import get_connection

vehicle_id = '46926fa9-ab15-42c4-9868-4d2a44b9d3ea'

with get_connection() as connection, connection.cursor() as cursor:
    cursor.execute(
        "SELECT * FROM vehicles WHERE vehicle_id = %s",
        (vehicle_id,)
        )

    result = cursor.fetchone()

    print(result)