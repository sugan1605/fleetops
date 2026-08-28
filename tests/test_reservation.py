from datetime import datetime

from app.customer import Customer
from app.reservation import Reservation
from app.vehicle import Vehicle


def test_reservation_creation():
    customer = Customer(
        customer_id=545,
        first_name="Losugan",
        last_name="Sivasuthan",
        phone_number="+47 21390016",
        email="test1@test.no",
    )

    vehicle = Vehicle(
        registration_number="DS 35637",
        make="Volvo",
        model="XC-60",
        fuel_type="Petrol",
        operational_status="AVAILABLE",
        odometer_km=7500,
    )

    # create reservation

    reservation = Reservation(
        customer=customer,
        vehicle=vehicle,
        start=datetime(2026, 9, 25, 17, 0),
        end=datetime(2026, 9, 30, 17, 0),
    )
