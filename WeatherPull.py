
# Made as a utility to debug data pull requests quickly, can be configured multiple ways to look at variety of aspects of pull

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
import matplotlib.pyplot as plt

# NOAA Individual access code
TOKEN = 'ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh'
# Base NOAA retrieval URLs
BASE_URL_DATA = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data/'
BASE_URL_STATIONS = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
# Geographical region for data being pulled (Currently: MN State)
LOCATION_ID = 'FIPS:27'
DATASET_ID = 'GHCND' #datset id for "Daily Summaries"
DATATYPE = 'TOBS'
# Temp at time of observation: 'TOBS'
# Max Daily Temp: 'TMAX'
# Min Daily Temp: 'TMIN'
# Precipitation (inches): 'PRCP'
# Snowfall amount (inches): 'SNOW'
# Snow on ground (inches): 'SNWD'

num_cols = 60
num_rows = 30

# Date range for data being pulled, [YYYY, MM, DD]
BeginDate = datetime.date(2018, 9, 29)

# max_rows = None
# max_cols = None
# pd.set_option("display.max_rows", max_rows, "display.max_columns", max_cols)

# MN encapsulating all and more of the stations the weateher data will come from)
df_stations = get_station_info(LOCATION_ID, DATASET_ID, TOKEN, BASE_URL_STATIONS)

# Weather data call
df_weather = get_weather(LOCATION_ID, DATASET_ID, DATATYPE, BeginDate, BeginDate, TOKEN, BASE_URL_DATA)

# Merge of station and weather data
df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')

station_objects = station_format(df)
# Set dimensions of temp grid (rows, cols)
temp_grid = np.zeros((num_rows, num_cols))
# Sets spacial parameters based on max and mins of long/lat of collected datat stations
xcords = (np.amin(np.array(df['longitude'])), np.amax(np.array(df['longitude'])))
ycords = (np.amin(np.array(df['latitude'])), np.amax(np.array(df['latitude'])))
print(xcords)
print(ycords)
# Formatting data into interpolated gridimgarray3 = imgarray.view('B')[:,::4]
grid = interp2d(station_objects, temp_grid, xcords, ycords, 3)

# Visualization of request points
visualize(df['longitude'], df['latitude'], df['value'])

# Visualization of interpolated data
xaxis = np.arange(np.amin(np.array(df['longitude'])), np.amax(np.array(df['longitude'])), (np.amax(np.array(df['longitude'])) - np.amin(np.array(df['longitude'])))/num_cols)
yaxis = np.arange(np.amin(np.array(df['latitude'])), np.amax(np.array(df['latitude'])), (np.amax(np.array(df['latitude'])) - np.amin(np.array(df['latitude'])))/num_rows)
gridx, gridy = np.meshgrid(xaxis, yaxis)
visualize(gridx, gridy, grid)

plt.show()
