# FleetOps Linux Deployment

## Prerequisites

- Ubuntu Linux server
- Git
- Docker
- Docker Compose
- SSH access to the server

---

## Initial Deployment

### 1. Connect to the server

```bash
ssh sugan@<server>
```

### 2. Clone the repository

```bash
git clone git@github.com:sugan1605/fleetops.git
cd fleetops
```

---

## Environment Configuration

FleetOps uses environment variables for database configuration.

Create a `.env` file in the project root:

```env
FLEETOPS_DB_PASSWORD=<your-password>
```

The `.env` file contains credentials and must not be committed to Git.

Verify that `.env` is ignored:

```bash
git check-ignore -v .env
```

---

## Verify the Environment

Check the installed versions:

```bash
docker --version
docker compose version
```

---

## Start FleetOps

Start the application and database:

```bash
docker compose up -d
```

---

## Verification

### Check Container Status

```bash
docker compose ps
```

Expected state:

- `api` → running
- `postgres` → running and healthy

### Verify the API

```bash
curl http://localhost:8000/health
```

### Test the Vehicle Endpoint

```bash
curl http://localhost:8000/vehicles
```

An empty array (`[]`) is valid if no vehicles have been added to the database.

---

## Inspect Logs

### API Logs

Show API logs from the last 10 minutes:

```bash
docker compose logs --since 10m api
```

### PostgreSQL Logs

Show PostgreSQL logs from the last 10 minutes:

```bash
docker compose logs --since 10m postgres
```

### Recent Logs

Show the latest 50 log lines from all services:

```bash
docker compose logs --tail=50
```

---

## Test the Database

Query the vehicles table directly:

```bash
docker compose exec postgres \
  psql -U creativity -d fleetops -c "SELECT * FROM vehicles;"
```

---

## Updating an Existing Deployment

Pull the latest changes from `main`:

```bash
git pull origin main
```

Rebuild and start the services:

```bash
docker compose up -d --build
```

Verify the deployment:

```bash
docker compose ps
```

Verify the API:

```bash
curl http://localhost:8000/health
```

Inspect recent API logs if needed:

```bash
docker compose logs --since 10m api
```

---

## Stopping FleetOps

Stop the services:

```bash
docker compose stop
```

Start them again:

```bash
docker compose start
```

---

## Recovering a Stopped API Container

Check the service state:

```bash
docker compose ps
```

Start the API:

```bash
docker compose start api
```

Verify recovery:

```bash
curl http://localhost:8000/health
```

---

## Troubleshooting

### API Cannot Be Reached

Check the container state:

```bash
docker compose ps
```

Inspect API logs:

```bash
docker compose logs --since 10m api
```

### PostgreSQL Is Unhealthy

Check the container state:

```bash
docker compose ps
```

Inspect PostgreSQL logs:

```bash
docker compose logs --since 10m postgres
```

### Inspect Recent API Requests

```bash
docker compose logs --since 2m api
```

### Inspect PostgreSQL Data

Open a PostgreSQL shell:

```bash
docker compose exec postgres \
  psql -U creativity -d fleetops
```

---

## Debugging Workflow

When something fails:

1. **Observe**
2. **Identify**
3. **Form a hypothesis**
4. **Test the hypothesis**
5. **Fix the problem**
6. **Verify recovery**
