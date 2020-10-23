# IMPORTED PACKAGES
#needed to make web requests
def weather_import(Token, BeginDate, EndDate, LocationID):
    import pandas as pd
    import numpy as np
    from WeatherReq import get_weather
    from StationReq import get_station_info
    import geopandas
    import matplotlib.pyplot as plt
    from scipy.interpolate import griddata
    import datetime
    # ------------------------------------------------------------------------------
    # Location & data category
    datasetid = 'GHCND' #datset id for "Daily Summaries"
    datatype = 'TOBS'
    start_date = datetime.date(BeginDate[0], BeginDate[1], BeginDate[2])
    end_date = datetime.date(EndDate[0], EndDate[1], EndDate[2])

    # Base NOAA retrivial URLs
    base_url_data = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/data/'
    base_url_stations = 'https://www.ncdc.noaa.gov/cdo-web/api/v2/stations'
    # ------------------------------------------------------------------------------
    # CALL, FORMATTING & SAVE

    delta = datetime.timedelta(days=1)
    df_weather = get_weather(LocationID, datasetid, datatype, start_date, start_date, Token, base_url_data)
    start_date += delta
    print('df_weather')
    print(df_weather)

    while start_date <= end_date:
        df = get_weather(LocationID, datasetid, datatype, start_date, start_date, Token, base_url_data)
        print('df')
        print(df)
        df_weather = df_weather.append(df, ignore_index = True)
        print('df_weather')
        print(df_weather)
        start_date += delta


    # Weather data call

    df_stations = get_station_info(LocationID, datasetid, Token, base_url_stations)
    df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')

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
    df.drop('date', inplace=True, axis=1)
    #
    # grid_x = np.array()
    # grid = griddata((df['longitude'], df['latitude']), df['value'], (grid_x, grid_y), method='nearest')
    # print(grid)
    # plt.plot(grid)
    # plt.show()

    # gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))
    # print(gdf.head())
    #
    # gdf.plot(color='red')
    # plt.show()


    # Save as csv
    df.to_csv('/Users/patrickgibbons/Desktop/git/WeatherPred/WeatherDataFiles/MNweather_'\
    +str(end_date)+'_noaa.csv', encoding='utf-8', index=False)

    # Notes from meeting 10/11/2020
    # Clean up syntax with Lintr
    # Compartmentalize with function to be bale to run of header function
    # Start getting working feed forward loop going eith tensorflow
    # Make it all packaged and modular
    # Look into ReactJS
