# CI Debugging Exercise

## Purpose

This exercise intentionally introduces a controlled failure into the
FleetOps CI pipeline to practice diagnosing and recovering from CI failures.

The failure will be introduced on the `feature/ci` branch and will not
represent a real application defect.

The goal is to practice the workflow used when a CI pipeline fails:

1. Identify the failing stage.
2. Read and interpret the CI logs.
3. Isolate the root cause.
4. Make the smallest appropriate fix.
5. Verify the fix locally where possible.
6. Push the correction.
7. Confirm that CI returns to a passing state.

## Baseline

Before introducing the failure, the FleetOps CI pipeline successfully:

- Installs Python dependencies
- Runs Ruff
- Builds the Docker image
- Initializes the PostgreSQL test database
- Runs the automated test suite

At the time of this exercise, the test suite contains 79 tests.


## Intentional Failure

_To be completed after the failure has been introduced._

### Failure observed

_To be completed._

### Failing CI stage

_To be completed._

### Error message

_To be completed._

## Investigation

_To be completed while diagnosing the failure._

### Steps taken

_To be completed._

## Root Cause

_To be completed after the root cause has been confirmed._

## Fix

_To be completed after the fix has been implemented._

## Verification

_To be completed after CI passes again._

Expected verification:

- Ruff passes
- Docker image builds successfully
- PostgreSQL initializes successfully
- Automated tests pass
- GitHub Actions returns to a passing state

## What I Learned

_To be completed after the exercise._

## Evidence

The GitHub Actions run containing the intentional failure and the
subsequent successful run provide the CI execution history for this exercise.
