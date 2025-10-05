from fastapi import APIRouter, Query
from app.utils.o3_by_coordinates import get_o3_by_coordinates
from app.models import O3ByCoordinatesResponse

router = APIRouter(prefix="/o3", tags=["O3"])

@router.get("/by-coordinates", response_model=O3ByCoordinatesResponse)
def get_o3(lat: float = Query(...), lon: float = Query(...)):
    """Returns the amount of O3 (DU) for a given location"""
    return get_o3_by_coordinates(lat, lon)
