import pandas as pd
import numpy as np
from StationObject import Station

def station_format(df):
    # Takes in information in combined stations and weather dataframe and returns array of station objects for interpolation function
    stations = []
    for i in range(len(df)):
        if df.loc[i, 'value'] < 150:
            var = Station(df.loc[i, 'value'], df.loc[i, 'longitude'], df.loc[i, 'latitude'])
            stations.append(var)
    # print('Array of Station objects created')
    Sarray = np.array(stations)
    return(Sarray)
