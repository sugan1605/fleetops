from fastapi import FastAPI

from app.api.routes import health

app = FastAPI()

app.include_router(health.router)

@app.get("/")
def root():
    return {"message": "FleetOps API is running"}

