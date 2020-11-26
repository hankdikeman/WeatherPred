
# Made as a utility to look in detail at data pull requests quickly, can be configured multiple ways

# IMPORTS
import pandas as pd
import numpy as np
from WeatherReq import get_weather
from StationReq import get_station_info
from interp2d import interp2d
import datetime
from interp2d import interp2d
from station_format import station_format
from day_num import day_num
from visualize import *

# NOAA Individual access code
TOKEN = 'ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh'
# Base NOAA retrieval URLs
BASE_URL_DATA = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data/'
BASE_URL_STATIONS = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
# Geographical region for data being pulled (Currently: MN State)
LOCATION_ID = 'FIPS:06'
DATASET_ID = 'GHCND' #datset id for "Daily Summaries"
DATATYPE = 'TAVG'
# Temp at time of observation: 'TOBS'
# Max Daily Temp: 'TMAX'
# Min Daily Temp: 'TMIN'
# Precipitation (inches): 'PRCP'
# Snowfall amount (inches): 'SNOW'
# Snow on ground (inches): 'SNWD'

# Date range for data being pulled, [YYYY, MM, DD]
BeginDate = datetime.date(2018, 9, 29)


# MN encapsulating all and more of the stations the weateher data will come from)
df_stations = get_station_info(LOCATION_ID, DATASET_ID, TOKEN, BASE_URL_STATIONS)
# Weather data call
df_weather = get_weather(LOCATION_ID, DATASET_ID, DATATYPE, BeginDate, BeginDate, TOKEN, BASE_URL_DATA)
# Merge of station and weather data
df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')

print(df)
visualize(df['longitude'], df['latitude'], df['value'])
