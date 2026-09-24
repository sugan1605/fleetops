from app.database import get_connection
from app.models.customer import Customer


class CustomerRepository:
    def _row_to_customer(self, row) -> Customer:
        (
            customer_id,
            customer_type,
            first_name,
            last_name,
            email,
            phone_number,
        ) = row

        return Customer(
            customer_id,
            customer_type,
            first_name,
            last_name,
            email,
            phone_number,
        )

    def add(self, customer: Customer):
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO customers"
                "(customer_id, customer_type, first_name, last_name, email, phone_number )"
                "VALUES(%s,%s,%s,%s,%s,%s)",
                (
                    customer.customer_id,
                    customer.customer_type,
                    customer.first_name,
                    customer.last_name,
                    customer.email,
                    customer.phone_number,
                ),
            )

    def get_all(self) -> list[Customer]:
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers;")

            results = cursor.fetchall()

            customers = []

            for result in results:
                customers.append(self._row_to_customer(result))

            return customers

    def get_by_id(self, customer_id: str) -> Customer | None:
        with get_connection() as connection, connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM customers WHERE customer_id = %s", (customer_id,)
            )

            result = cursor.fetchone()

            if not result:
                return None

            customer = self._row_to_customer(result)

            return customer
