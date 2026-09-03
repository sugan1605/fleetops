from typing import ClassVar


class Customer:
    customer_types: ClassVar[dict[str, str]] = {
        "WORKSHOP": "WS",
        "BUSINESS": "BU",
        "LEISURE": "LE",
        "PARTNER": "PA",
    }

    def __init__(
        self,
        customer_id: str,
        customer_type: str,
        first_name: str,
        last_name: str,
        email: str,
        phone_number: str,
    ):

        if customer_type not in self.customer_types:
            raise ValueError("invalid customer type, please choose right customer type")

        expected_prefix = self.customer_types[customer_type]

        if not customer_id.startswith(expected_prefix):
            raise ValueError("The customer type doesn't match with customer ID!")

        self.customer_id = customer_id
        self.customer_type = customer_type
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
