# IMPORTED PACKAGES
#needed to make web requests
def weather_import(Token, BeginDate, EndDate, StationID):
    import pandas as pd
    import numpy as np
    from WeatherReq import get_weather
    # ------------------------------------------------------------------------------
    # EXTRA PARAMETERS
    mytoken = Token

    # Date range
    begin_date = BeginDate
    end_date = EndDate

    # Location & data category
    datasetid = 'GHCND' #datset id for "Daily Summaries"
    datatype = 'TOBS'
    stationid = StationID

    # Base NOAA retrivial URLs
    base_url_data = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data/'
    # ------------------------------------------------------------------------------
    # CALL, FORMATTING & SAVE

    # Weather data call
    df_weather = get_weather(stationid, datasetid, datatype, begin_date, end_date, mytoken, base_url_data)

    print(df_weather)

    # Drop unneeded columns
    df_weather.drop('attributes', inplace=True, axis=1)
    df_weather.drop('station', inplace=True, axis=1)
    df_weather.drop('datatype', inplace=True, axis=1)

    # Save as csv
    df_weather.to_csv('/Users/patrickgibbons/Desktop/WeatherData/weather_'\
    +str(stationid)+'_noaa.csv', encoding='utf-8', index=False)

    # Notes from meeting 10/11/2020
    # Clean up syntax with Lintr
    # Compartmentalize with function to be bale to run of header function
    # Start getting working feed forward loop going eith tensorflow
    # Make it all packaged and modular
    # Look into ReactJS
