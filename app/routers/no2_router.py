from fastapi import APIRouter, Query
from app.utils.no2_by_coordinates import get_no2_by_coordinates
from app.models import NO2ByCoordinatesResponse

router = APIRouter(prefix="/no2", tags=["NO2"])

@router.get("/by-coordinates", response_model=NO2ByCoordinatesResponse)
def get_no2(lat: float = Query(...), lon: float = Query(...)):
    """
     Returns the amount of NO2 (moléculas/cm²) for a given location
    """
    return get_no2_by_coordinates(lat, lon)
