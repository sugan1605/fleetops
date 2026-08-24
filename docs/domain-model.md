# FleetOps Domain Model

FleetOps is a fictional fleet and rental operations platform inspired by
real-world car rental workflows.

This document describes the initial domain model and will evolve as the
system requirements become clearer.

---

## Core Entities

### Vehicle

Represents a physical vehicle in the fleet.

A vehicle has:

- Registration number
- Make
- Model
- Fuel type
- Vehicle group
- Odometer mileage
- Status
- Equipment

The registration number must be unique.

Example:

```text
Registration: AB12345
Make: Toyota
Model: RAV4
Fuel type: Petrol
Group: U
Odometer: 84,230 km
Status: Available

## Business Rules To Define

## Business Rules

### Reservation Conflicts

A vehicle must not be assigned to overlapping reservations.

Example:

Reservation A:
10:00 → 14:00

Reservation B:
13:00 → 16:00

The system must reject the second assignment.

### Vehicle Availability

A vehicle must not be assigned during a period where it is blocked
for maintenance, damage, sale, or another reservation.