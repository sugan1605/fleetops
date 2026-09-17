# FleetOps 🚗

A fictional fleet and rental operations platform inspired by real-world
car rental workflows.


## Purpose

FleetOps is a hands-on project where I am building a rental operations
system from the ground up.

I use the project to improve my Python and software engineering skills,
while gradually introducing technologies used in Cloud and DevOps.

The idea is simple: start with the rental lifecycle and build the
engineering around it step by step.


## Core Rental Lifecycle

The core rental lifecycle is currently in place.

The system currently handles:

- Customer validation
- Vehicle validation
- Vehicle availability
- Time-based vehicle blocks
- Reservations
- Rental validation
- Active rentals
- Vehicle returns
- Early, on-time, and late returns
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
- Git and Github
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
- Rental returns
- Early, on-time, and late returns
- Rental state changes
- Vehicle check-in
- Odometer updates
- Vehicle operational status changes
- Invalid inputs and business rules

**Current status: 47 tests passing**

Run the test suite with:

```bash
python3 -m pytest
```


## Project Status

🚧 **Core Rental Lifecycle v1 — Complete**

The core rental domain is implemented and covered by automated tests.

The next phase will focus on building the application and infrastructure
around the domain, starting with the API and database before moving into
containerization, CI/CD, cloud infrastructure, and Kubernetes.