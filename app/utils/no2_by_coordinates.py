import earthaccess
import xarray as xr
import numpy as np

def get_no2_by_coordinates(lat: float, lon: float, date: str):
    auth = earthaccess.login(persist=True)
    short_name = "TEMPO_NO2_L3"
    version = "V03"
    date_start = f"{date} 00:00:00"
    date_end = f"{date} 23:59:59"

    results = earthaccess.search_data(
        short_name=short_name,
        version=version,
        temporal=(date_start, date_end),
        point=(lon, lat),
    )

    if not results:
        return {"error": "No se encontraron datos para las coordenadas indicadas"}

    files = earthaccess.open(results[:1])
    ds = xr.open_datatree(files[0], phony_dims="sort")

    prod = ds.product
    var = prod.variables["vertical_column_troposphere"]
    tropospheric_no2 = var[:]
    fill_value = var.encoding.get("_FillValue")
    tropospheric_no2 = np.where(tropospheric_no2 == fill_value, np.nan, tropospheric_no2)

    mean_no2 = float(np.nanmean(tropospheric_no2))
    return {"lat": lat, "lon": lon, "date": date, "no2_moleculas_cm2": mean_no2}
