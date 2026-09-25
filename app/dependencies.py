from app.repositories.customer_repository import CustomerRepository
from app.repositories.reservation_repository import ReservationRepository
from app.repositories.vehicle_repository import VehicleRepository

vehicle_repository = VehicleRepository()
customer_repository = CustomerRepository()


reservation_repository = ReservationRepository(
    customer_repository=customer_repository,
    vehicle_repository=vehicle_repository,
)


def get_vehicle_repository():
    return vehicle_repository


def get_customer_repository():
    return customer_repository


def get_reservation_repository():
    return reservation_repository
