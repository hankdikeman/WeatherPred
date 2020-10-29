# IMPORTED PACKAGES
#needed to make web requests
def weather_import(Token, BeginDate, EndDate, LocationID, horz_dims, vert_dims, pval):
    import pandas as pd
    import numpy as np
    from WeatherReq import get_weather
    from StationReq import get_station_info
    from interp2d import interp2d
    import datetime
    from interp2d import interp2d
    from station_format import station_format
    from gen_format import gen_format
    from day_num import day_num
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
    # Format training data array
    days = day_num(start_date, end_date)
    train_data = np.empty((0, vert_dims))

    # Station data call
    df_stations = get_station_info(LocationID, datasetid, Token, base_url_stations)

    # Set date iteration for while loop
    delta = datetime.timedelta(days=1) # time step for dates

    while start_date <= end_date:
        # Weather data call
        df_weather = get_weather(LocationID, datasetid, datatype, start_date, start_date, Token, base_url_data)
        # Merge of station and weather data
        df = df_weather.merge(df_stations, left_on = 'station', right_on = 'id', how='inner')
        # Formatting data into interpolated grid
        grid = gen_format(df, horz_dims, vert_dims, pval)
        # Save single data grid to larger training data array (current problem getting grid to transfer into train_data correctly)
        train_data = np.append(train_data, grid, axis = 0)
        start_date += delta
    print('Weather data retrieved')

    # Return numpy grid of temperature values
    print('Training data from ' + str(BeginDate) + ' to ' + str(EndDate) + ' returned')
    return(train_data)
