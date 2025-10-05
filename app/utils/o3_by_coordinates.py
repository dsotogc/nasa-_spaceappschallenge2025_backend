import earthaccess
import xarray as xr
import numpy as np
from datetime import datetime, timezone, timedelta

def get_o3_by_coordinates(lat: float, lon: float): # units are du
    auth = earthaccess.login(persist=True)
    short_name = "TEMPO_O3TOT_L3"
    version = "V03"
    # Take current UTC datetime but force the year to 2022 as government shutdown, we have no actual data
    now_utc = datetime.now(timezone.utc)
    try:
        now_2022 = now_utc.replace(year=2022)
    except ValueError:
        # handle rare cases like Feb 29 -> fallback to Feb 28
        now_2022 = now_utc.replace(year=2022, day=28)

    # Format as "YYYY-MM-DD HH:MM:SS"
    date_end = now_2022.strftime("%Y-%m-%d %H:%M:%S")
    date_start = (now_2022 - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")

    results = earthaccess.search_data(
        short_name=short_name,
        version=version,
        temporal=(date_start, date_end),
        point=(-76.3868, 37.1036), # Test data, as we are not in tempo satellite area
    )

    if not results:
        return {"error": "We couldnt find data for your location"}

    files = earthaccess.open(results[:1])
    ds = xr.open_datatree(files[0], phony_dims="sort")

    prod = ds.product
    var = prod.variables["column_amount_o3"]
    O3_column = var[:]

    mean_o3 = float(np.nanmean(O3_column))
    return mean_o3
