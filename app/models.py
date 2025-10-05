from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Location(BaseModel):
    lat: float
    lon: float

class AirQualityReading(BaseModel):
    timestamp: datetime
    pm25: Optional[float]
    pm10: Optional[float]
    no2: Optional[float]
    o3: Optional[float]
    co: Optional[float]

class AQIResponse(BaseModel):
    lat: float
    lon: float
    no2_column_molecules_cm2: float
    estimated_ppb: float
    estimated_ug_m3: float
    aqi_value: float
    aqi_category: str


class LatestResponse(BaseModel):
    location: Location
    readings: List[AirQualityReading]


class NO2ByCoordinatesResponse(BaseModel):
    lat: float
    lon: float
    date: str
    no2_molecules_cm2: float


class O3ByCoordinatesResponse(BaseModel):
    lat: float
    lon: float
    date: str
    o3_du: float
