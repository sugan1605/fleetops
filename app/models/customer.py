from typing import ClassVar


class Customer:
    # Centralized mapping between customer types and their ID prefixes.
    # Keeping this in one place avoids hardcoding the same business rule
    # throughout the application.

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

        # First and last name are mandatory fields in the FleetOps
        # customer domain.
        self._validate_required_name(first_name)
        self._validate_required_name(last_name)

        if not email and not phone_number:
            raise ValueError(
                "Please provide email or phone number to continue, both can't be empty."
            )

        # Only supported customer types should be allowed into the domain model.
        if customer_type not in self.customer_types:
            raise ValueError("invalid customer type, please choose right customer type")

        # The customer ID must follow the convention defined for its type.
        expected_prefix = self.customer_types[customer_type]

        if not customer_id.startswith(expected_prefix):
            raise ValueError("The customer type doesn't match with customer ID!")

        # Store the validated customer data on this Customer instance.
        self.customer_id = customer_id
        self.customer_type = customer_type
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number

    def _validate_required_name(self, name: str):
        # Name validation is shared by object creation and name updates,
        # so the rule is kept in one reusable helper.
        if not name:
            raise ValueError("Name is required.")

    def edit_first_name(self, new_first_name: str):
        # Validate before modifying state so the Customer object
        # can never be updated with an invalid required name.
        self._validate_required_name(new_first_name)
        self.first_name = new_first_name

    def edit_last_name(self, new_last_name: str):
        # Apply the same validation rule when the last name is changed.
        self._validate_required_name(new_last_name)
        self.last_name = new_last_name

    def edit_phone_number(self, new_phone_number: str):
        # A customer must always retain at least one contact method.
        # Validate the proposed state before changing the object.
        if not new_phone_number and not self.email:
            raise ValueError("There must be at least one contact method.")

        self.phone_number = new_phone_number

    def edit_email(self, new_email: str):
        # The same contact rule applies when changing the email:
        # removing the email is only allowed when a phone number exists.
        if not new_email and not self.phone_number:
            raise ValueError("There must be at least one contact method.")

        self.email = new_email
