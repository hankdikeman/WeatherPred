import matplotlib.pyplot as plt
import numpy as np


null_data = np.ones(shape = (17500))
csv_data = np.genfromtxt('FlaskPage/USTrainData1_1_2002TO9_17_2004.csv', delimiter=',')[:,:-4]

count = 0
for row in range(np.shape(csv_data)[0]):
    data_line = np.reshape(csv_data[row,:], newshape = (17500))
    for col in range(np.shape(data_line)[0]):
        if (data_line[col] != 0 and null_data[col] == 1):
            null_data[col] = 0
            print("boing " + str(count))
            count = count+1

null_data = null_data.reshape(100,175)

with open('FlaskPage/static/no_stations_mask.npy', 'wb') as filename:
    np.save(filename, null_data)
