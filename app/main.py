from fastapi import FastAPI, Query
from .data_cliente import get_latest_mock, convertir_no2_a_aqi
from fastapi.middleware.cors import CORSMiddleware
from .models import LatestResponse, AQIResponse, Location
from app.routers import no2_router, o3_router
from .utils import no2_by_coordinates as no22, o3_by_coordinates as o33, get_aqi as aqii


app = FastAPI(title="NASA Air Quality Backend")

def get_aqi_endpoint(lat: float, lon: float):
    no2 = no22.get_no2_by_coordinates(lat, lon)
    o3 = o33.get_o3_by_coordinates(lat, lon)
    aqi = aqii.compute_aqi(no2, o3)
    return {"aqi": round(aqi)}

app.include_router(no2_router.router)

app.include_router(o3_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/latest", response_model=LatestResponse)
async def get_latest(lat: float, lon: float):
    data = await get_latest_mock(lat, lon)
    return data


@app.get("/api/aqi")
def calcular_aqi(lat: float = Query(...), lon: float = Query(...)):
    """Calculate AQI using coordinates (combined NO2+O3) via utils.get_aqi.compute_aqi_from_coordinates."""
    result = aqii.compute_aqi_from_coordinates(lat, lon)
    return result

@app.get("/")
async def root():
    return {"message": "Backend de NASA Air Quality funcionando"}

