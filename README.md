# FleetOps 🚗

FleetOps is a fictional fleet and rental operations platform inspired by real-world car rental workflows.

I'm building it to strengthen my Python skills and learn how applications are built, tested, deployed and operated. My main focus is DevOps and platform engineering.

## What it does

FleetOps models the core rental lifecycle, including:

- Customer and vehicle validation
- Vehicle availability and time-based blocks
- Reservations and vehicle assignment
- Rental extensions and overlap prevention
- Vehicle returns and rental completion
- Employee check-in, odometer and fuel recording
- Vehicle condition and operational status management
- Vehicle preparation before it becomes available again

## Engineering and DevOps

I'm using FleetOps to practise the tools and workflows involved in delivering and operating software.

- **Python:** application logic and business rules
- **PostgreSQL and SQL:** relational data and database integration
- **pytest:** automated testing
- **Ruff:** linting and code quality
- **Docker:** containerised application and non-root execution
- **Git and GitHub:** version control, branches and pull requests
- **GitHub Actions:** automated testing, linting and Docker image builds
- **Linux:** deployment, logs, service troubleshooting and recovery

## Homelab

I use a homelab built around an Ubuntu Linux VM to practise operational tasks in a controlled environment.

This gives me hands-on experience with:

- Linux administration and command-line troubleshooting
- SSH and remote access
- Running and inspecting Docker containers
- Container networking and application-to-database connectivity
- Service health, logs and recovery
- Running the FleetOps API as a non-root user

The homelab lets me experiment, troubleshoot failures and document what I learn without relying on a continuously running cloud environment.

## Continuous Integration

FleetOps uses GitHub Actions to validate changes automatically.

The CI pipeline:

1. Sets up Python and installs dependencies.
2. Runs Ruff checks.
3. Starts PostgreSQL for integration tests.
4. Initialises the test database.
5. Runs the automated test suite.
6. Builds the Docker image.

The pipeline helps catch problems before changes are merged into `main`.

I've also documented a hands-on CI debugging exercise where I investigated a failed database initialisation step, identified a configuration mismatch and verified the fix through a successful pipeline run.

## Testing

FleetOps uses `pytest` for automated testing, integrated into GitHub Actions.

The test suite covers domain logic, validation, repository behaviour, vehicle availability, reservations, rental workflows, returns and operational status changes.

Run the tests locally:

```bash
python -m pytest
```

Run the code quality checks:

```bash
ruff check .
```

## Project Structure

```text
fleetops/
├── app/
├── docker/
│   └── postgres/
│       └── init.sql
├── docs/
│   ├── ci-debugging-exercise.md
│   ├── domain-model.md
│   └── linux-deployment.md
├── scripts/
├── tests/
├── .github/
│   └── workflows/
├── Dockerfile
├── compose.yaml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Current Focus

The core rental lifecycle is implemented and covered by automated tests. The project has progressed into containerisation, Linux operations and CI.

My next steps are Azure Container Registry, Terraform, Kubernetes, deployment automation, monitoring and security.

## How I Work

Understand → Design → Build → Test → Debug → Improve

I prefer learning by building, breaking things, investigating the cause and fixing them. FleetOps gives me a practical environment to develop those habits while connecting software development with DevOps and platform engineering.