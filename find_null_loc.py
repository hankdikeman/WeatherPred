"""
This file collects points over the mesh grid that are uncaptured by NOAA data pull and generates a binary mask that can be used to filter out the displayed weather. Performed by determining where in the weather data values of 0 are reported consistently
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
import matplotlib.pyplot as plt
import numpy as np

# declare mask arrays
zero_data = np.zeros(shape = (17500))
# read data from csv
csv_data = np.genfromtxt('FlaskPage/USTrainData1_1_2002TO9_17_2004.csv', delimiter=',')[:,:-4]

count = 0
for row in range(np.shape(csv_data)[0]):
    data_line = np.reshape(csv_data[row,:], newshape = (17500))
    for col in range(np.shape(data_line)[0]):
        if (data_line[col] != 0 and zero_data[col] == 0):
            zero_data[col] = 1
            print("boing " + str(count))
            count = count+1

zero_data = zero_data.reshape(100,175)

with open('FlaskPage/static/no_stations_mask.npy', 'wb') as filename:
    np.save(filename, zero_data)
