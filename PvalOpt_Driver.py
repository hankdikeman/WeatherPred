# Driver for Pval Opt

import pandas as pd
import numpy as np
from PvalOpt_DataFormat import PvalOpt_DataFormat
from StationObject import Station
from visualize import visualize
from interp2d import interp2d
from PvalOpt_FindIndex import PvalOpt_FindIndex

# Retrieve formatted data just to get length of data for given day
data, min_log, max_log, min_lat, max_lat = PvalOpt_DataFormat()

# Set dimensions of temp grid
horz_dims = 50
vert_dims = 50
temp_grid = np.zeros((horz_dims, vert_dims))

# List of possible p vals
pvals = np.arange(1, 15, 1)
# Initilize output data to be saved
opt_pval_save = np.zeros(len(data))
opt_dif_save = np.zeros(len(data))

for j in range(len(data)):
    # Remove one data point from retrieved dataset and save as seperate variable
    removed_station = data[j]
    select_data = np.delete(data, j)
    if ((removed_station.lon > -95 and removed_station.lon < -92) and (removed_station.lat > 44 and removed_station.lat < 47)):
        # Sets spacial parameters based on max and mins of long/lat of collected datat stations
        xcords = (min_log, max_log)
        ycords = (min_lat, max_lat)
        # Finds indexs of grid data that represent temperature of removed point
        rs_x, rs_y = PvalOpt_FindIndex(removed_station, horz_dims, vert_dims, xcords, ycords)
        # Initialize values to be saved
        opt_pval = None
        opt_dif = None
        val_dif = 100

        for i in pvals:
            # Formatting data into interpolated gridimgarray3 = imgarray.view('B')[:,::4]
            grid = interp2d(select_data, temp_grid, xcords, ycords, i)
            dif = abs(grid[rs_x][rs_y]-removed_station.temp)
            if (dif < val_dif):
                val_dif = dif
                opt_pval = i
                opt_dif = dif

        print('\n\nPoint ' + str(j+1) + ' Pval: ' + str(opt_pval))
        print('Point ' + str(j+1) + ' temp difference: ' + str(opt_dif))
            # opt_pval_save[j] = opt_pval
            # opt_dif_save[j] = opt_dif

# print(opt_pval_save)
# print(opt_dif_save)
