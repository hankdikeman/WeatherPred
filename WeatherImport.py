# IMPORTED PACKAGES
#needed to make web requests
import requests
import pandas as pd
import numpy as np
import os
import datetime
import sys
# ------------------------------------------------------------------------------
# DATA FETCHING FUNCTION
def get_weather(stationid, datasetid, datatype, begin_date, end_date, mytoken, base_url):
    token = {'token': mytoken}
    params = 'datasetid='+str(datasetid)+'&'+'stationid='+str(stationid)+'&'+'datatypeid='+str(datatype)+'&'+'startdate='+str(begin_date)+'&'+'enddate='+str(end_date)+'&'+'limit=1000'+'&'+'units=standard'
    r = requests.get(base_url, params = params, headers=token)
    print("Request status code: "+str(r.status_code))

    #results comes in json form. Convert to dataframe
    df = pd.DataFrame.from_dict(r.json()['results'])
    return df
    # 'datatypeid='+str(datatype)
# ------------------------------------------------------------------------------
# PARAMETERS

# API interaction set up
mytoken = 'ExHqFtwmXTLwOevojJsTbCcgZdlVYuRh'

# Date range
lastyear = datetime.datetime.now()-datetime.timedelta(days=730)
now = datetime.datetime.now()-datetime.timedelta(days=365)

# Format for the API request
begin_date = lastyear.strftime("%Y-%m-%d")
end_date = now.strftime("%Y-%m-%d")
print(begin_date)

# Location & data category
stationid = 'GHCND:USC00214373'
datasetid = 'GHCND' #datset id for "Daily Summaries"
datatype = 'TOBS'

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
df_weather.to_csv('/Users/patrickgibbons/Desktop/WeatherData/weather_'+str(stationid)+'_noaa.csv', encoding='utf-8', index=False)
