from fastapi import FastAPI

from app.api.routes import health, vehicle

app = FastAPI()

app.include_router(health.router)
app.include_router(vehicle.router)

@app.get("/")
def root():
    return {"message": "FleetOps API is running"}

