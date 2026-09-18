# FleetOps 🚗

A fictional fleet and rental operations platform inspired by real-world
car rental workflows.


## Purpose

FleetOps is a hands-on project where I am building a rental operations
system from the ground up.

I use the project to strengthen my Python and software engineering skills
while progressively introducing technologies and practices used in Cloud
and DevOps.

The idea is simple: start with the rental lifecycle and build the
engineering around it step by step.


## Core Rental Lifecycle

The project currently covers the core domain logic for vehicles,
customers, reservations and rentals.

The system handles:

- Customer validation
- Vehicle validation
- Vehicle availability
- Time-based vehicle blocks
- Reservations
- Vehicle assignment
- Rental validation
- Rental extensions
- Prevention of overlapping rentals
- Active rentals
- Vehicle returns
- Early, on-time and late returns
- Rental completion when a vehicle is returned
- Employee check-in
- Odometer and fuel recording
- Vehicle condition recording
- Vehicle `DIRTY` status after check-in
- Returning a prepared vehicle to `AVAILABLE`


### Current lifecycle

```text
AVAILABLE
    ↓
RESERVED
    ↓
ON_A_RENT
    ↓
Customer returns vehicle
    ↓
Rental COMPLETED
    ↓
Employee check-in
    ↓
Vehicle DIRTY
    ↓
Cleaning / preparation
    ↓
AVAILABLE
```


## Engineering Focus

The project will progressively cover:

- Python
- REST APIs
- PostgreSQL
- SQL and data modelling
- Automated testing
- Error handling
- Docker
- Git and GitHub
- CI/CD
- Azure
- Infrastructure as Code with Terraform
- Kubernetes
- Monitoring and observability
- Security and configuration management


## Project Structure

```text
fleetops/
├── app/
│   ├── models/
│   ├── services/
│   └── main.py
├── docs/
├── tests/
├── .gitignore
├── pyproject.toml
└── README.md
```


## Testing

FleetOps uses `pytest` for automated testing.

The tests currently cover:

- Customer and rental validation
- Vehicle availability
- Vehicle blocks
- Vehicle assignment
- Rental extensions
- Rental overlap prevention
- Rental returns
- Early, on-time, and late returns
- Rental state changes
- Vehicle check-in
- Odometer updates
- Vehicle operational status changes
- Invalid inputs and business rules

**Current status: 61 tests passing**

Run the test suite with:

```bash
python3 -m pytest
```

Run the code quality checks with:

```bash
ruff check .
```


## Project Status

🚧 **Core Rental Lifecycle — In Progress **

The core rental domain is implemented and covered by automated tests.

Current development is focused on completing the reservation-to-rental workflow.

The next phase will expand the application around the domain, starting with the
API and database before progressively introducing containerization, CI/CD, cloud infrastructure
and Kubernetes.


## Development Philosophy

FleetOps is developed through hands-on problem solving:

Understand
    ↓
Design
    ↓
Build
    ↓
Test
    ↓
Debug
    ↓
Improve
    ↓
Commit

The goal is to build a realistic project while developing an understanding
of how software engineering and DevOps practices work together.
