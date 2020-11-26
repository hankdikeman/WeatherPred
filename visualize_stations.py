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
