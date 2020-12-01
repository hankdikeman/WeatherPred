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
from token_cycle import *
from visualize_stations import *
import matplotlib.pyplot as plt


def TOBS_US_weather_pull(Date):
    # NOAA Individual access code (will be cycled through later in function)
    TOKEN = 'ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh'
    # Base NOAA retrieval URLs
    BASE_URL_DATA = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data/'
    BASE_URL_STATIONS = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
    # Geographical region for data being pulled (Currently: MN State)
    LOCATION_ID_NUM = np.array(['01', '04', '05', '06', '08', '09', '10', '11', '12', '13', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56'])
    LOCATION_ID_STR = 'FIPS:'
    DATASET_ID = 'GHCND' #datset id for "Daily Summaries"
    DATATYPE = 'TOBS'
    # Temp at time of observation: 'TOBS'
    # Max Daily Temp: 'TMAX'
    # Min Daily Temp: 'TMIN'
    # Precipitation (inches): 'PRCP'
    # Snowfall amount (inches): 'SNOW'
    # Snow on ground (inches): 'SNWD'


    # get interpolation dimensions from interpshape parameter
    HORZ_DIMS = 100
    VERT_DIMS = 50
    # set p-value for inverse distance weighted interp
    pval = 2.5
    # ------------------------------------------------------------------------------

    # Initialize training data and station array
    train_data = np.empty((0, VERT_DIMS*HORZ_DIMS))
    US_station_objects = np.array([])


    for i in LOCATION_ID_NUM:
        LOCATION_ID = LOCATION_ID_STR + i
        # print('State num: ' + LOCATION_ID )
        # Station data call
        df_stations = get_station_info((LOCATION_ID_STR + str(i)), DATASET_ID, TOKEN, BASE_URL_STATIONS)
        # Weather data call
        df_weather = get_weather((LOCATION_ID_STR + str(i)), DATASET_ID, DATATYPE, Date, Date, TOKEN, BASE_URL_DATA)
        # Merge of station and weather data
        df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')
        # print('Length of pull: ' + str(len(df)))
        # Coverting combined station and weather data into a np.array of station objects and adding them to overall station objects for entire US
        US_station_objects = np.append(US_station_objects, station_format(df))
        # print(str(len(US_station_objects)))

        TOKEN = token_cycle(TOKEN)

    # print('Retrieved data from all states')
    visualize_stations(US_station_objects)
    US_station_objects = np.array(US_station_objects)
    # Set dimensions of temp grid
    temp_grid = np.zeros((VERT_DIMS, HORZ_DIMS))
    # Sets spacial parameters based on US geography x direction longitude (65, 125), y direction latitude (25, 50)
    xcords = (-125, -60)
    ycords = (25, 50)
    # Formatting data into interpolated gridimgarray3 = imgarray.view('B')[:,::4]
    grid = interp2d(US_station_objects, temp_grid, xcords, ycords, pval)
    # print('Interpolation complete')
    # Save single data grid to larger training data array (current problem getting grid to transfer into train_data correctly)
    train_data = np.vstack((train_data, grid.flatten()))
    # print('Weather data retrieved')

    # Return numpy grid of temperature values
    return(train_data)
    print('Training data from ' + str(Date) + ' returned')

    xaxis = np.arange(-125, -65, (125 - 65)/HORZ_DIMS)
    yaxis = np.arange(25, 50, (50 - 25)/VERT_DIMS)
    gridx, gridy = np.meshgrid(xaxis, yaxis)
    visualize(gridx, gridy, grid)
    plt.show()
