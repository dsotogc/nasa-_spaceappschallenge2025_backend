def no2_to_ppb(no2_molecules_cm2):
    # 1 molecula/cm2 ≈ 2.69e16 molecules/m3
    # Conversión aproximada a ppb para AQI
    return no2_molecules_cm2 / 1e15

def o3_to_ppb(o3_dobson_units):
    # 1 DU ≈ 2.69e16 molecules/m2
    # Aproximación para AQI (ppb)
    return o3_dobson_units * 2

def compute_aqi(no2_molecules_cm2, o3_dobson_units):
    no2_ppb = no2_to_ppb(no2_molecules_cm2)
    o3_ppb = o3_to_ppb(o3_dobson_units)

    # Niveles considerados normales para PM2.5, PM10, CO y SO2
    pm25_ppb = 12
    pm10_ppb = 50
    co_ppb = 1
    so2_ppb = 20

    no2_aqi = calculate_individual_aqi(no2_ppb, 'no2')
    o3_aqi = calculate_individual_aqi(o3_ppb, 'o3')
    pm25_aqi = calculate_individual_aqi(pm25_ppb, 'pm25')
    pm10_aqi = calculate_individual_aqi(pm10_ppb, 'pm10')
    co_aqi = calculate_individual_aqi(co_ppb, 'co')
    so2_aqi = calculate_individual_aqi(so2_ppb, 'so2')

    return max(no2_aqi, o3_aqi, pm25_aqi, pm10_aqi, co_aqi, so2_aqi)

def calculate_individual_aqi(conc, pollutant):
    breakpoints = {
        'pm25': [(0,12,0,50),(12.1,35.4,51,100),(35.5,55.4,101,150),(55.5,150.4,151,200),(150.5,250.4,201,300),(250.5,350.4,301,400),(350.5,500.4,401,500)],
        'pm10': [(0,54,0,50),(55,154,51,100),(155,254,101,150),(255,354,151,200),(355,424,201,300),(425,504,301,400),(505,604,401,500)],
        'no2': [(0,53,0,50),(54,100,51,100),(101,360,101,150),(361,649,151,200),(650,1249,201,300),(1250,1649,301,400),(1650,2049,401,500)],
        'so2': [(0,35,0,50),(36,75,51,100),(76,185,101,150),(186,304,151,200),(305,604,201,300),(605,804,301,400),(805,1004,401,500)],
        'co': [(0,4.4,0,50),(4.5,9.4,51,100),(9.5,12.4,101,150),(12.5,15.4,151,200),(15.5,30.4,201,300),(30.5,40.4,301,400),(40.5,50.4,401,500)],
        'o3': [(0,54,0,50),(55,70,51,100),(71,85,101,150),(86,105,151,200),(106,200,201,300),(201,300,301,400),(301,400,401,500)],
    }
    for bp in breakpoints[pollutant]:
        if bp[0] <= conc <= bp[1]:
            return ((bp[3]-bp[2])/(bp[1]-bp[0]))*(conc-bp[0])+bp[2]
    return 500


def compute_aqi_from_coordinates(lat: float, lon: float):
    """Fetch NO2 and O3 for the given coordinates and compute a combined AQI.

    Returns a dict with raw values and the computed AQI.
    """
    # Local imports to avoid top-level dependency issues
    try:
        from .no2_by_coordinates import get_no2_by_coordinates
        from .o3_by_coordinates import get_o3_by_coordinates
    except Exception:
        return {"error": "utils not available"}

    # Fetch values (utils may return a float or a dict)
    no2_res = get_no2_by_coordinates(lat, lon)
    if isinstance(no2_res, dict):
        no2_val = no2_res.get('no2_molecules_cm2') or no2_res.get('no2_moleculas_cm2')
    else:
        no2_val = no2_res

    o3_res = get_o3_by_coordinates(lat, lon)
    if isinstance(o3_res, dict):
        o3_val = o3_res.get('o3_du') or o3_res.get('O3_DU')
    else:
        o3_val = o3_res

    # Validate
    if no2_val is None or o3_val is None:
        return {"error": "could not retrieve pollutant values", "no2": no2_res, "o3": o3_res}

    # Compute combined AQI (uses existing helpers)
    try:
        aqi_value = compute_aqi(no2_val, o3_val)
    except Exception as e:
        return {"error": f"aqi computation failed: {e}"}

    return {
        "lat": lat,
        "lon": lon,
        "no2_molecules_cm2": no2_val,
        "o3_du": o3_val,
        "aqi": round(aqi_value)
    }
