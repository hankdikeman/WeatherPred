"""
Identical to station format file in root directory of repo. Compiles weather data stored in pandas dataframe and converts it to a numpy list of Station objects. Used during database updates for Flask sites.
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
import pandas as pd
import numpy as np
from StationObject import Station


def station_format(df):
    # Takes in information in combined stations and weather dataframe and returns array of station objects for interpolation function
    stations = []
    for i in range(len(df)):
        if df.loc[i, 'value'] < 150:
            var = Station(df.loc[i, 'value'],
                          df.loc[i, 'longitude'], df.loc[i, 'latitude'])
            stations.append(var)
    # print('Array of Station objects created')
    Sarray = np.array(stations)
    return(Sarray)
