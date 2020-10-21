# IMPORTED PACKAGES
#needed to make web requests
def weather_import(Token, BeginDate, EndDate, LocationID):
    import pandas as pd
    import numpy as np
    from WeatherReq import get_weather
    from StationReq import get_station_info
    # ------------------------------------------------------------------------------

    # Location & data category
    datasetid = 'GHCND' #datset id for "Daily Summaries"
    datatype = 'TOBS'

    # Base NOAA retrivial URLs
    base_url_data = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data/'
    base_url_stations = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
    # ------------------------------------------------------------------------------
    # CALL, FORMATTING & SAVE

    # Weather data call
    df_weather = get_weather(LocationID, datasetid, datatype, BeginDate, EndDate, Token, base_url_data)
    df_stations = get_station_info(LocationID, datasetid, Token, base_url_stations)
    df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')

    print(df)
    #Check for missing overlap between station weather info and location info

    # location_ismissing = df_weather[~df_weather['station'].isin(df_stations['id'])]
    # loc_miss_count = len(location_ismissing['station'].unique())
    # if loc_miss_count != 0:
    #     print("Missing location data for "+str(loc_miss_count)+" stations")
    # else:
    #     print("Successfully retrieved and combined location data")
    # Drop unneeded columns
    df.drop('attributes', inplace=True, axis=1)
    df.drop('station', inplace=True, axis=1)
    df.drop('datatype', inplace=True, axis=1)
    df.drop('datacoverage', inplace=True, axis=1)
    df.drop('elevation', inplace=True, axis=1)
    df.drop('elevationUnit', inplace=True, axis=1)
    df.drop('id', inplace=True, axis=1)
    df.drop('maxdate', inplace=True, axis=1)
    df.drop('mindate', inplace=True, axis=1)
    df.drop('name', inplace=True, axis=1)

    # Save as csv
    df.to_csv('/Users/patrickgibbons/Desktop/git/WeatherPred/WeatherDataFiles/MNweather_'\
    +str(BeginDate)+'_noaa.csv', encoding='utf-8', index=False)

    # Notes from meeting 10/11/2020
    # Clean up syntax with Lintr
    # Compartmentalize with function to be bale to run of header function
    # Start getting working feed forward loop going eith tensorflow
    # Make it all packaged and modular
    # Look into ReactJS
