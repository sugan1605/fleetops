from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def healt_check():
    return {"status": "ok"}