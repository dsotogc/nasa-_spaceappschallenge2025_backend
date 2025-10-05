from datetime import datetime, timezone
from .models import AirQualityReading, Location, LatestResponse

async def get_latest_mock(lat: float, lon: float):
    """
    Devuelve un mock de lectura de calidad del aire para la ubicación indicada.
    Todos los timestamps son UTC-aware.
    """
    # Timestamp actual con zona horaria UTC
    now_utc = datetime.now(timezone.utc)

    # Crear lectura de ejemplo
    reading = AirQualityReading(
        timestamp=now_utc,
        pm25=12.3,
        pm10=20.1,
        no2=5.2,
        o3=10.0,
        co=0.3
    )
    locationn = Location(lat=lat, lon=lon)

    return LatestResponse(location=locationn, readings=[reading])

# app/utils/data_cliente.py

def convertir_no2_a_aqi(no2_molecules_cm2: float):
    """
    Convierte una columna de NO2 (molecules/cm²) en un índice AQI estimado.
    """

    # 1. Aproximar concentración en ppb (factor empírico)
    estimated_ppb = no2_molecules_cm2 * 0.376e-15

    # 2. Convertir a µg/m³ (1 ppb NO2 ≈ 1.88 µg/m³)
    estimated_ug_m3 = estimated_ppb * 1.88

    # 3. Calcular AQI basado en rangos EPA
    breaks = [
        (0, 53, 0, 50, "Good"),
        (54, 100, 51, 100, "Moderate"),
        (101, 360, 101, 150, "Unhealthy for Sensitive Groups"),
        (361, 649, 151, 200, "Unhealthy"),
        (650, 1249, 201, 300, "Very Unhealthy"),
        (1250, 2049, 301, 400, "Hazardous")
    ]

    aqi_value = 0
    category = "Unknown"
    for c_low, c_high, aqi_low, aqi_high, cat in breaks:
        if c_low <= estimated_ppb <= c_high:
            aqi_value = ((aqi_high - aqi_low) / (c_high - c_low)) * (estimated_ppb - c_low) + aqi_low
            category = cat
            break

    return {
        "no2_column_molecules_cm2": no2_molecules_cm2,
        "estimated_ppb": round(estimated_ppb, 3),
        "estimated_ug_m3": round(estimated_ug_m3, 3),
        "aqi_value": round(aqi_value, 1),
        "aqi_category": category
    }
