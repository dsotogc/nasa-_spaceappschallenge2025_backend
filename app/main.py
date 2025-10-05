from fastapi import FastAPI, Query
from .data_cliente import get_latest_mock, convertir_no2_a_aqi
from fastapi.middleware.cors import CORSMiddleware
from .models import LatestResponse, AQIResponse, Location


app = FastAPI(title="NASA Air Quality Backend")

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


@app.post("/api/aqi", response_model=AQIResponse)
def calcular_aqi(location: Location):
    resultado = convertir_no2_a_aqi(location.no2_column_molecules_cm2)
    return AQIResponse(
        lat=location.lat,
        lon=location.lon,
        **resultado
    )

@app.get("/")
async def root():
    return {"message": "Backend de NASA Air Quality funcionando"}

