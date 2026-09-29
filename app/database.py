import os

import psycopg


def get_connection():
    database_name = os.getenv("FLEETOPS_DB_NAME", "fleetops")
    return psycopg.connect(f"dbname={database_name} user=creativity")
