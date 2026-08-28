from datetime import datetime


class VehicleBlock:
    VALID_BLOCK_TYPES = (
        "RESERVATION",
        "MAINTENANCE",
        "DAMAGE",
        "FOR_SALE",
    )

    def __init__(
        self, block_type: str, start: datetime, end: datetime, block_reason: str
    ):
        self.block_type = block_type
        self.start = start
        self.end = end
        self.block_reason = block_reason

        if not self.validate_block_type():
            raise ValueError("Invalid block type")

        if self.end < self.start:
            raise ValueError("end date can't be earlier than start date.")

    def validate_block_type(self):
        return self.block_type in self.VALID_BLOCK_TYPES


class Vehicle:
    VALID_OPERATIONAL_STATUSES = (
        "AVAILABLE",
        "RESERVED",
        "RENTED",
    )

    VALID_FUEL_TYPES = (
        "Petrol",
        "Diesel",
        "Electric",
    )

    def __init__(
        self,
        registration_number: str,
        make: str,
        model: str,
        fuel_type: str,
        operational_status: str = "AVAILABLE",
        odometer_km: int = 0,
    ):
        self.registration_number = registration_number
        self.make = make
        self.model = model
        self.fuel_type = fuel_type
        self.operational_status = operational_status
        self.blocks = []
        if not self.validate_fuel_type():
            raise ValueError("Invalid Fuel type")
        self.odometer_km = odometer_km
        if odometer_km < 0:
            raise ValueError("The km cannot be less than 0")
        if not self.validate_operational_status():
            raise ValueError("Invalid Status")

    def is_available(self, start: datetime, end: datetime):
        if end < start:
            raise ValueError("End date can't be earlier than start date")

        for block in self.blocks:
            if start <= block.end and end >= block.start:
                return False

        return True

    def add_block(self, block):
        if not isinstance(block, VehicleBlock):
            raise TypeError("Invalid block type!")

        self.blocks.append(block)

    def get_blocks(self):
        return list(self.blocks)

    def is_blocked(self, check_time: datetime):
        for block in self.blocks:
            if check_time >= block.start and check_time <= block.end:
                return True
        return False

    def update_odometer(self, new_odometer_km):
        if new_odometer_km < self.odometer_km:
            raise ValueError(
                "The updated km can't be less than or lower than current km"
            )
        if new_odometer_km < 0:
            raise ValueError("The updated km can't be less than 0")
        self.odometer_km = new_odometer_km

    def validate_fuel_type(self):
        return self.fuel_type in self.VALID_FUEL_TYPES

    def validate_operational_status(self):
        return self.operational_status in self.VALID_OPERATIONAL_STATUSES

    def update_operational_status(self, new_status):
        if new_status not in self.VALID_OPERATIONAL_STATUSES:
            raise ValueError("Invalid operational status")

        self.operational_status = new_status
