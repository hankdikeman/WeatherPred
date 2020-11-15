import pandas as pd
import numpy as np
from WeatherReq import get_weather
from StationReq import get_station_info
import datetime
from station_format import station_format
from StationObject import Station

# Parameters: station = integer between 0-40 represents staion that will be deleted
def PvalOpt_DataFormat():
    # NOAA Individual access code
    TOKEN = 'ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh'
    # Base NOAA retrieval URLs
    BASE_URL_DATA = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data/'
    BASE_URL_STATIONS = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
    # Geographical region for data being pulled (Currently: MN State)
    LOCATION_ID = 'FIPS:27'
    DATASET_ID = 'GHCND' #datset id for "Daily Summaries"
    DATATYPE = 'TOBS'

    # Date being pulled (Patricks birth date)
    start_date = datetime.date(1998, 9, 29)

    # MN encapsulating all and more of the stations the weateher data will come from)
    df_stations = get_station_info(LOCATION_ID, DATASET_ID, TOKEN, BASE_URL_STATIONS)
    # Weather data call
    df_weather = get_weather(LOCATION_ID, DATASET_ID, DATATYPE, start_date, start_date, TOKEN, BASE_URL_DATA)
    # Merge of station and weather data
    df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')
    # Retrieve max and min longitude and latitude
    min_log = np.amin(np.array(df['longitude']))
    max_log = np.amax(np.array(df['longitude']))
    min_lat = np.amin(np.array(df['latitude']))
    max_lat = np.amax(np.array(df['latitude']))

    # Coverting combined station and weather data into a np.array of station objects
    station_objects = station_format(df)

    return((station_objects, min_log, max_log, min_lat, max_lat))
