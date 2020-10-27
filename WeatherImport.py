# IMPORTED PACKAGES
#needed to make web requests
def weather_import(Token, BeginDate, EndDate, LocationID):
    import pandas as pd
    import numpy as np
    from WeatherReq import get_weather
    from StationReq import get_station_info
    from StationObject import Station
    from interp2d import interp2d
    import geopandas
    import matplotlib.pyplot as plt
    import datetime
    from interp2d import interp2d
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

    while start_date <= end_date:
        df = get_weather(LocationID, datasetid, datatype, start_date, start_date, Token, base_url_data)
        df_weather = df_weather.append(df, ignore_index = True)
        start_date += delta
    print('Weather data retrieved')

    # Weather data call
    df_stations = get_station_info(LocationID, datasetid, Token, base_url_stations)
    df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')
    print('Station data merged with weather data')

    # Visualize raw data without interpolation
    lons=np.array(df['longitude'])
    lats=np.array(df['latitude'])
    data=np.array(df['value'])
    fig = plt.figure()
    plt.scatter(lons, lats, c=data, cmap='viridis')
    plt.colorbar()
    plt.show()

    # Coverting station data into a np.array of station objects
    stations = np.empty(shape=(len(df),), dtype=object)
    for i in range(len(df)):
        var = Station(df.loc[i, 'value'], df.loc[i, 'longitude'], df.loc[i, 'latitude'])
        stations[i] = var
    print('Array of Station objects created')

    # Run interpolation
    hor_step = 100
    vert_step = 100
    temp_grid = np.zeros((hor_step,vert_step))
    space_grid = np.zeros((hor_step,vert_step))
    xcords = (np.amin(lons), np.amax(lons))
    ycords = (np.amin(lats), np.amax(lats))
    pval = 5
    grid = interp2d(stations, temp_grid, xcords, ycords, pval)
    print('Array of interpolated temperatures created')

    # Visualize interpolation data output
    xaxis = np.arange(np.amin(lons), np.amax(lons), ((np.amax(lons)-np.amin(lons))/(hor_step)))
    yaxis = np.arange(np.amin(lats), np.amax(lats), ((np.amax(lats)-np.amin(lats))/(vert_step)))
    gridx, gridy = np.meshgrid(xaxis, yaxis)
    print(gridx)
    print(gridy)
    fig2 = plt.figure()
    plt.scatter(gridx, gridy, c=grid, cmap='viridis')
    plt.colorbar()
    plt.show()
    plt.plot

    # Return numpy grid of temperature values
    print('Temp grid returned')
    print(grid)
    return(grid)



    # myInterval = ot.Interval([-97., 43.5], [-89.5, 49.])




    # gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))
    # print(gdf.head())
    #
    # gdf.plot(color='red')
    # plt.show()


    # Save as csv
    # df.to_csv('/Users/patrickgibbons/Desktop/git/WeatherPred/WeatherDataFiles/MNweather_'\
    # +str(end_date)+'_noaa.csv', encoding='utf-8', index=False)

    # df.drop('attributes', inplace=True, axis=1)
    # df.drop('station', inplace=True, axis=1)
    # df.drop('datatype', inplace=True, axis=1)
    # df.drop('datacoverage', inplace=True, axis=1)
    # df.drop('elevation', inplace=True, axis=1)
    # df.drop('elevationUnit', inplace=True, axis=1)
    # df.drop('id', inplace=True, axis=1)
    # df.drop('maxdate', inplace=True, axis=1)
    # df.drop('mindate', inplace=True, axis=1)
    # df.drop('name', inplace=True, axis=1)
    # df.drop('date', inplace=True, axis=1)


    #  temp_grid is an empty 2d numpy array
