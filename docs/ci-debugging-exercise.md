# CI Debugging Exercise

## Purpose

This exercise simulates a teammate introducing an unexpected change to the FleetOps CI configuration. The goal was to practise investigating an unfamiliar CI failure, identifying the root cause, implementing a minimal fix, and verifying recovery.

## Baseline

Before the exercise, the FleetOps CI pipeline successfully:

- Installs Python dependencies
- Runs Ruff linting
- Builds the Docker image
- Initializes the PostgreSQL test database
- Runs the automated test suite

The test suite contained 79 tests at the time of the exercise.

## Failure

**Failing stage:** Initialize database

**Observed error:**

```text
psql: error: connection to server at "localhost" (::1),
port 5432 failed: FATAL: database "fleetops_ci" does not exist
```

GitHub Actions exited with code 2.

## Investigation

The investigation followed the available evidence rather than assuming PostgreSQL itself was broken.

1. Inspected the failed GitHub Actions step and its error output.
2. Distinguished a database-selection error from a server connectivity failure.
3. Used `sed -n '15,30p' .github/workflows/ci.yml` to inspect the CI environment and PostgreSQL service configuration.
4. Compared `FLEETOPS_DB_NAME` with the PostgreSQL service's `POSTGRES_DB` setting.
5. Confirmed that the initialization command attempted to connect to a database name that the service had not created.

## Root Cause

The CI workflow contained inconsistent database configuration:

- `FLEETOPS_DB_NAME` was set to `fleetops_ci`.
- `POSTGRES_DB` was set to `fleetops`.

The initialization step used `FLEETOPS_DB_NAME` to select the database for its first `psql` connection. PostgreSQL initialized `fleetops`, but the command attempted to connect to `fleetops_ci`.

Because that database did not exist, the connection failed before the `CREATE DATABASE fleetops_test` statement could execute.

The root cause was a **CI configuration mismatch**, not a Python application defect or a PostgreSQL server startup failure.

## Fix

Changed the workflow environment variable to match the database created by the PostgreSQL service:

```yaml
FLEETOPS_DB_NAME: fleetops
```

No application code or database schema changes were required.

## Verification

After the correction, GitHub Actions completed successfully.

- Ruff linting passed.
- Docker image build passed.
- PostgreSQL initialization passed.
- The automated test suite passed.
- The workflow returned to a green state.

**Evidence:**

- Failed run: CI #10, commit `c1be3e2` — `test: simulate CI configuration change`
- Successful recovery: CI #11, commit `2572676` — `fix: correct CI database configuration`

## What I Learned

- Read the first meaningful error instead of guessing at the cause.
- A reachable database server does not guarantee that the requested database exists.
- Compare environment variables with service initialization settings.
- `psql -d` selects the database to connect to; SQL commands cannot execute until that connection succeeds.
- Local Docker Compose behavior and GitHub Actions service configuration are separate environments.
- A small, evidence-based configuration fix is preferable to changing multiple components at once.
- A passing CI run after the correction provides evidence that the failure was resolved.

## Debugging Workflow

Observe → Reproduce where possible → Inspect → Isolate → Fix → Verify → Document.
