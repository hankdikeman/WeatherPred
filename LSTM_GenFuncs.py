"""
This file generates and returns LSTM models of different architectures and sizes in order to predict future weather states
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

def Gen_LSTM_Basic(long_nodes, lat_nodes, day_num):
    LSTM_model = models.Sequential()
    # LSTM 1: return sequences because we have more LSTM layers
    LSTM_model.add(layers.LSTM(128, return_sequences=True,
                               input_shape=(day_num, long_nodes * lat_nodes)))
    # LSTM_model.add(layers.Dropout(0.2))
    # LSTM 2: return sequences because we have more LSTM layers
    # LSTM_model.add(layers.LSTM(256, return_sequences=True))
    # LSTM_model.add(layers.Dropout(0.2))
    # LSTM 3: return sequences because we have more LSTM layers
    # LSTM_model.add(layers.LSTM(256, return_sequences=True))
    # LSTM_model.add(layers.Dropout(0.2))
    # LSTM 4: no return sequences because we have dense next
    LSTM_model.add(layers.LSTM(256))
    LSTM_model.add(layers.Dropout(0.2))
    # Dense output layer, 1 for now
    LSTM_model.add(layers.Dense(256, activation='relu'))
    LSTM_model.add(layers.Dense(512, activation='relu'))
    LSTM_model.add(layers.Dense(lat_nodes * long_nodes, activation='tanh'))
    # compile
    LSTM_model.compile(
        optimizer='adam', loss='mean_squared_error', metrics=['mse'])
    # return model
    return LSTM_model

# LSTM model 2 with different loss and shorter layer seq


def short_LSTM(long_nodes, lat_nodes, day_num):
    # declare model
    LSTM_short = models.Sequential()
    # 2 LSTM layers
    # LSTM_short.add(layers.LSTM(512, return_sequences=True,
    #                            input_shape=(day_num, long_nodes * lat_nodes),
    #                            dropout=0.2, recurrent_dropout=0.2
    #                            ))
    LSTM_short.add(layers.LSTM(512,
                               return_sequences=False,
                               dropout=0.2
                               ))
    # add dense processing layer
    LSTM_short.add(layers.Dense(256, activation='relu'))
    # add dense output layer
    LSTM_short.add(layers.Dense(long_nodes * lat_nodes, activation='tanh'))
    # compile LSTM model
    LSTM_short.compile(loss='mean_squared_error',
                       optimizer="adam", metrics=['mse'])
    # return model
    return LSTM_short


def LSTM_BatchNorm(long_nodes, lat_nodes, day_num):
    return 0


def LSTM_GRU(long_nodes, lat_nodes, day_num):
    return 0

# convolutional processing after LSTM processing, then dense layers


def LSTM_toConv(long_nodes, lat_nodes, day_num):
    # declare model
    LSTM_conv = models.Sequential()
    # 2 LSTM layers
    LSTM_conv.add(layers.LSTM(128,
                              return_sequences=True,
                              input_shape=(day_num, long_nodes * lat_nodes),
                              dropout=0.2,
                              recurrent_dropout=0.2
                              ))
    LSTM_conv.add(layers.LSTM(512,
                              return_sequences=True,
                              dropout=0.2
                              ))
    # add convolutional processing layer
    LSTM_conv.add(layers.Conv1D(128,
                                kernel_size=5,
                                activation='relu'))
    # flatten from convolutional processing
    LSTM_conv.add(layers.Flatten())
    # two dense processing layers
    LSTM_conv.add(layers.Dense(256, activation='relu'))
    LSTM_conv.add(layers.Dense(256, activation='relu'))
    # add dense output layer
    LSTM_conv.add(layers.Dense(long_nodes * lat_nodes, activation='tanh'))
    # compile LSTM model
    LSTM_conv.compile(loss='mean_squared_error',
                      optimizer="adam", metrics=['mse'])
    # return model
    return LSTM_conv
