import os

import psycopg

def get_connection():
    database_host = os.getenv("FLEETOPS_DB_HOST", "localhost")
    database_name = os.getenv("FLEETOPS_DB_NAME", "fleetops")
    database_user = os.getenv("FLEETOPS_DB_USER", "creativity")
    database_password = os.getenv("FLEETOPS_DB_PASSWORD")

    return psycopg.connect(
        host=database_host,
        dbname=database_name,
        user=database_user,
        password=database_password,
            )
