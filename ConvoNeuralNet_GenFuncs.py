import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# generates and returns convolutional model based on following parameters:
# long_nodes = node num west to east, lat_nodes = node num north to south
# day_num = number of days modelled, num_fil = number of filters used
def Gen_CNN_Basic(long_nodes, lat_nodes, day_num, num_fil):
    # declare model
    CNN_model = models.Sequential()
    # 1 convolutional layer with num_fil 3x3 filters
    CNN_model.add(layers.Conv2D(num_fil,
                                (3,3),
                                activation = 'relu',
                                input_shape = (long_nodes, lat_nodes, day_num)))
    # 2x2 pooling layer
    CNN_model.add(layers.MaxPooling2d((2, 2)))
    # 2nd convolutional layer
    CNN_model.add(layers.Conv2D(num_fil,
                                (3,3),
                                activation = 'relu'))
    # 2nd 2x2 pooling layer
    CNN_model.add(layers.MaxPooling2d((2, 2)))
    # 3rd convolutional layer
    CNN_model.add(layers.Conv2D(num_fil,
                                (3,3),
                                activation = 'relu'))
    # 3rd pooling layer
    CNN_model.add(layers.MaxPooling2d((2, 2)))
    # flatten output to 1 dimension
    CNN_model.add(layers.Flatten())
    # 1st dense layer with 64 nodes
    CNN_model.add(layers.Dense(64,
                               activation = 'relu'))
    # output layer with map for long and lat
    CNN_model.add(layers.Dense(long_nodes*lat_nodes))
    # return generated model
    return CNN_model

####
#   CNN number 2
#   insert model generation function here
####

####
#   CNN number 3
#   insert model generation function here
####
