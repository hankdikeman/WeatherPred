# Function to format combined station and weather dataframe into numpy area with spatial grid characteristics
from station_format import station_format
import numpy as np
import pandas as pd
from interp2d import interp2d

def gen_format(df, hor_step, vert_step, pval):

    # Coverting combined station and weather data into a np.array of station objects
    stations = station_format(df)

    # Set dimensions of temp grid
    temp_grid = np.zeros((hor_step,vert_step))
    # Sets spacial parameters based on max and mins of long/lat of collected stations
    xcords = (np.amin(np.array(df['longitude'])), np.amax(np.array(df['longitude'])))
    ycords = (np.amin(np.array(df['latitude'])), np.amax(np.array(df['latitude'])))
    # Run interpolation
    grid = interp2d(stations, temp_grid, xcords, ycords, pval)
    print('Array of interpolated temperatures created')

    # # **NOTE** Visualizations only for single day data, should not be used usually
    # # Visualize raw data without interpolation
    # visualize(np.array(df['longitude']), np.array(df['latitude']), np.array(df['value']))
    #
    # # Visualize interpolation data output
    # xaxis = np.arange(np.amin(np.array(df['longitude'])), np.amax(np.array(df['longitude'])), ((np.amax(np.array(df['longitude']))-np.amin(np.array(df['longitude'])))/(hor_step)))
    # yaxis = np.arange(np.amin(np.array(df['latitude'])), np.amax(np.array(df['latitude'])), ((np.amax(np.array(df['latitude']))-np.amin(np.array(df['latitude'])))/(vert_step)))
    # gridx, gridy = np.meshgrid(xaxis, yaxis)
    # visualize(gridx, gridy, grid)
    return(grid)
