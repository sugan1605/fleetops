CREATE TABLE vehicles (
    vehicle_id UUID PRIMARY KEY,
    registration_number TEXT NOT NULL UNIQUE,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    fuel_type TEXT NOT NULL,
    operational_status TEXT NOT NULL,
    odometer_km INTEGER NOT NULL CHECK (odometer_km >= 0)
);

CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_type TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT NOT NULL UNIQUE
);

CREATE TABLE reservations (
    reservation_id UUID PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    vehicle_id UUID REFERENCES vehicles(vehicle_id),
    start_at TIMESTAMPTZ NOT NULL,
    end_at TIMESTAMPTZ NOT NULL
);
