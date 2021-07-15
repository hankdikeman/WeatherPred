"""
Driver for minimum distance weighting optimization. This was used to determine optimum distance weighting for IDW
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
import pandas as pd
import numpy as np
from PvalOpt_DataFormat import PvalOpt_DataFormat
from StationObject import Station
from visualize import visualize
from interp2d import interp2d
from PvalOpt_FindIndex import PvalOpt_FindIndex
from PvalOpt_DistanceFrom import closest_distance
import matplotlib.pyplot as plt

# Retrieve formatted data just to get length of data for given day
data, min_log, max_log, min_lat, max_lat = PvalOpt_DataFormat()

# Set dimensions of temp grid
horz_dims = 100
vert_dims = 100
temp_grid = np.zeros((horz_dims, vert_dims))

# List of possible p vals
pvals = np.arange(1, 15, 1)

# Visualize map
# xcords = (min_log, max_log)
# ycords = (min_lat, max_lat)
# grid = interp2d(data, temp_grid, xcords, ycords, 2.5)
#
#
# # # Visualize interpolation data output
# xaxis = np.arange(min_log, max_log, (max_log - min_log)/horz_dims)
# yaxis = np.arange(min_lat, max_lat, (max_lat - min_lat)/vert_dims)
# print(xaxis)
# gridx, gridy = np.meshgrid(xaxis, yaxis)
# visualize(gridx, gridy, grid)


Initilize output data to be saved
opt_pval_save = np.zeros(len(data))
opt_dif_save = np.zeros(len(data))
opt_dist_save = np.zeros(len(data))

for j in range(len(data)):
    # Remove one data point from retrieved dataset and save as seperate variable
    removed_station = data[j]
    select_data = np.delete(data, j)
    if ((removed_station.lon > -95 and removed_station.lon < -92) and (removed_station.lat > 44 and removed_station.lat < 47)):
        # Find distance to closest station for removed point
        distance = closest_distance(removed_station, select_data)
        # Sets spacial parameters based on max and mins of long/lat of collected datat stations
        xcords = (min_log, max_log)
        ycords = (min_lat, max_lat)
        # Finds indexs of grid data that represent temperature of removed point
        rs_x, rs_y = PvalOpt_FindIndex(removed_station, horz_dims, vert_dims, xcords, ycords)
        # Initialize values to be saved
        opt_pval = None
        opt_dif = None
        val_dif = 100

        point_dif_save = np.zeros(len(pvals))

        for i in range(len(pvals)):
            # Formatting data into interpolated gridimgarray3 = imgarray.view('B')[:,::4]
            grid = interp2d(select_data, temp_grid, xcords, ycords, pvals[i])
            dif = abs(grid[rs_x][rs_y]-removed_station.temp)
            point_dif_save[i] = dif

            if (dif < val_dif):
                val_dif = dif
                opt_pval = pvals[i]
                opt_dif = dif

        plt.plot(pvals, point_dif_save, linewidth=2)
        plt.xlabel('pval')
        plt.ylabel('diff')

        print('\n\nPoint ' + str(j+1) + ' Pval: ' + str(opt_pval))
        print('Point ' + str(j+1) + ' temp difference: ' + str(opt_dif))
        print('Point ' + str(j+1) + ' closest station distance: ' + str(distance))
        opt_pval_save[j] = opt_pval
        opt_dif_save[j] = opt_dif
        opt_dist_save[j] = distance
plt.show()

plt.scatter(opt_pval_save, opt_dif_save, c=opt_dist_save, cmap='viridis')
plt.xlabel('Opt Pval')
plt.ylabel('Temp difference')
plt.colorbar()
plt.show()
print(opt_pval_save)
print(opt_dif_save)
