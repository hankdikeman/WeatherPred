import pandas as pd
import numpy as np
from StationObject import Station

def station_format(df):
    # Takes in information dataframe of initial data pulled and returns array of station objects for interpolation function
    stations = np.empty(shape=(len(df),), dtype=object)
    for i in range(len(df)):
        var = Station(df.loc[i, 'value'], df.loc[i, 'longitude'], df.loc[i, 'latitude'])
        stations[i] = var
    print('Array of Station objects created')
    return(stations)
