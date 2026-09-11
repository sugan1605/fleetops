class Customer:
    customer_types = ("WORKSHOP", "BUSINESS", "LEISURE", "PARTNER")

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
            raise ValueError(
                "invalid customer type, please choose right customer type!"
            )

        self.customer_id = customer_id
        self.customer_type = customer_type
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
