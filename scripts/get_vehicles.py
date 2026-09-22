from app.database import get_connection

with get_connection() as connection, connection.cursor() as cursor:
    cursor.execute("SELECT * FROM vehicles;")

    result = cursor.fetchall()

    print(result)