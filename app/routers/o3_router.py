from fastapi import APIRouter, Query
from app.utils.o3_by_coordinates import get_o3_by_coordinates

router = APIRouter(prefix="/o3", tags=["O3"])

@router.get("/by-coordinates")
def get_o3(lat: float = Query(...), lon: float = Query(...), date: str = Query(...)):
    """
    Devuelve la cantidad de O3 (DU) para una ubicación y fecha dadas
    """
    return get_o3_by_coordinates(lat, lon, date)
