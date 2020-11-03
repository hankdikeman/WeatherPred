import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np

# generates and returns convolutional model based on following parameters:
# x_len = stations west to east, y_len = stations north to south
# day_num = number of days modelled, num_fil = number of filters used
def Gen_CNN_Basic(x_len, y_len, day_num, num_fil):
    # declare model
    CNN_model = models.Sequential()
    # 1 convolutional layer with num_fil 3x3 filters
    CNN_model.add(layers.Conv2D(num_fil,
                                (3,3),
                                activation = 'relu',
                                input_shape = (x_len, y_len, day_num)))
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
    # output layer with 1 output node (for temp)
    CNN_model.add(layers.Dense(1))
    # return generated model
    return CNN_model
