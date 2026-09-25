from fastapi import FastAPI

from app.api.routes import health, reservation, vehicle

app = FastAPI()

app.include_router(health.router)
app.include_router(reservation.router)
app.include_router(vehicle.router)

@app.get("/")
def root():
    return {"message": "FleetOps API is running"}

