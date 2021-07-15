"""
Visualization of station objects by first placing into pandas dataframe, then calling general visualization function
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from visualize import *

def visualize_stations(stations):

    data = []
    for i in stations:
        data.append([i.temp, i.lon, i.lat])

    df = pd.DataFrame(data, columns=['value', 'longitude', 'latitude'])

    visualize(df['longitude'], df['latitude'], df['value'])
