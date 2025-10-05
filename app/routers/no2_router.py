from fastapi import APIRouter, Query
from app.utils.no2_by_coordinates import get_no2_by_coordinates

router = APIRouter(prefix="/no2", tags=["NO2"])

@router.get("/by-coordinates")
def get_no2(lat: float = Query(...), lon: float = Query(...), date: str = Query(...)):
    """
    Devuelve la cantidad de NO2 (moléculas/cm²) para una ubicación y fecha dadas
    """
    return get_no2_by_coordinates(lat, lon, date)
