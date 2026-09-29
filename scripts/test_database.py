from uuid import uuid4

from app.database import get_connection

vehicle_id = uuid4()

with get_connection() as connection, connection.cursor() as cursor:
    cursor.execute("SELECT current_database(), current_user")
    result = cursor.fetchone()

    print(result)