"""
This program pulls weather from the state of MN and returns. Receives date range of pull as parameter
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
import pandas as pd
import numpy as np
from WeatherReq import get_weather
from StationReq import get_station_info
from interp2d import interp2d
import datetime
from interp2d import interp2d
from station_format import station_format
from day_num import day_num


def PullMNWeather(DateRange):
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

    # Date range for data being pulled, [YYYY, MM, DD]
    BeginDate = DateRange[0]
    EndDate = DateRange[1]

    # get interpolation dimensions from interpshape parameter
    horz_dims = 50
    vert_dims = 50
    # set p-value for inverse distance weighted interp
    pval = 4
    # ------------------------------------------------------------------------------
    # Format dates with Datetime package
    start_date = BeginDate
    end_date = EndDate
    # Set a time step of one day for iterating through dates
    DELTA = datetime.timedelta(days=1)
    # Calculate how many days are in date range with function day_num
    # **Look for a datetime package to do this
    days = day_num(start_date, end_date)

    # Initialize training data array
    train_data = np.empty((0, vert_dims*horz_dims))

    # Pull station data (can be done before anything else because it will pull data for all stations in
    # MN encapsulating all and more of the stations the weateher data will come from)
    df_stations = get_station_info(LOCATION_ID, DATASET_ID, TOKEN, BASE_URL_STATIONS)

    # loop through date range pulling data one at a time
    while start_date <= end_date:
        # Weather data call
        df_weather = get_weather(LOCATION_ID, DATASET_ID, DATATYPE, start_date, start_date, TOKEN, BASE_URL_DATA)
        # Merge of station and weather data
        df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')
        # Coverting combined station and weather data into a np.array of station objects
        station_objects = station_format(df)
        # Set dimensions of temp grid
        temp_grid = np.zeros((horz_dims, vert_dims))
        # Sets spacial parameters based on max and mins of long/lat of collected datat stations
        xcords = (np.amin(np.array(df['longitude'])), np.amax(np.array(df['longitude'])))
        ycords = (np.amin(np.array(df['latitude'])), np.amax(np.array(df['latitude'])))
        # Formatting data into interpolated gridimgarray3 = imgarray.view('B')[:,::4]
        grid = interp2d(station_objects, temp_grid, xcords, ycords, pval)
        # Save single data grid to larger training data array (current problem getting grid to transfer into train_data correctly)
        train_data = np.vstack((train_data, grid.flatten()))
        start_date += DELTA
        print("one day done")
    print('Weather data retrieved')

    # Return numpy grid of temperature values
    print('Training data from ' + str(BeginDate) + ' to ' + str(EndDate) + ' returned')
    return(train_data)
