from datetime import datetime

import pytest

from app.customer import Customer
from app.reservation import Reservation
from app.vehicle import Vehicle



# Test fixtures
@pytest.fixture
def test_customer():
    customer = Customer(
        customer_id=5656,
        first_name="Losugan",
        last_name="Sivasuthan",
        email="ssv1605@test.com",
        phone_number="+47 21390016",

    )

    return customer

@pytest.fixture
def test_vehicle():
    vehicle = Vehicle(
     registration_number="DS 35637",
     make="Volvo",
     model="XC-60",
     fuel_type="Petrol",
     operational_status="AVAILABLE",
     odometer_km=7500,

     )

    return vehicle

def test_reservation_creation(test_customer, test_vehicle):
    

   

    start = datetime(2026, 9, 25, 17, 0)
    end = datetime(2026, 9, 20, 17, 0)

    # create reservation
    with pytest.raises(ValueError):
        Reservation(
            customer=test_customer,
            vehicle=test_vehicle,
            start=start,
            end=end,
        )


def test_reservation_is_active(test_customer, test_vehicle):

    start = datetime(2026, 9, 25, 17, 0)
    end = datetime(2026, 9, 30, 17, 0)

    reservation = Reservation(customer=test_customer, vehicle=test_vehicle, start=start, end=end)

    assert reservation.is_active(datetime(2026, 9, 27, 12, 0))
