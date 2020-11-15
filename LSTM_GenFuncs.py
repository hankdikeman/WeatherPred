import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# first LSTM model
def Gen_LSTM_Basic(long_nodes, lat_nodes, day_num):
    LSTM_model = models.Sequential()
    # LSTM 1: return sequences because we have more LSTM layers
    LSTM_model.add(layers.LSTM(256, return_sequences=True, input_shape = (day_num,long_nodes*lat_nodes) ))
    LSTM_model.add(layers.Dropout(0.2))
    # LSTM 2: return sequences because we have more LSTM layers
    LSTM_model.add(layers.LSTM(256, return_sequences=True))
    LSTM_model.add(layers.Dropout(0.2))
    # LSTM 3: return sequences because we have more LSTM layers
    LSTM_model.add(layers.LSTM(256, return_sequences=True))
    LSTM_model.add(layers.Dropout(0.2))
    # LSTM 4: no return sequences because we have dense next
    LSTM_model.add(layers.LSTM(256))
    LSTM_model.add(layers.Dropout(0.2))
    # Dense output layer, 1 for now
    LSTM_model.add(layers.Dense(512, activation='relu'))
    LSTM_model.add(layers.Dense(lat_nodes*long_nodes, activation='sigmoid'))
    # compile
    LSTM_model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mse'])
    # return model
    return LSTM_model

# LSTM model 2 with different loss and shorter layer seq
def short_LSTM(long_nodes, lat_nodes, day_num):
    # declare model
    LSTM_short = models.Sequential()
    # 2 LSTM layers
    LSTM_short.add(layers.LSTM(512, return_sequences=True,
                        input_shape=(day_num, long_nodes*lat_nodes),
                        dropout=0.2, recurrent_dropout=0.2
                        ))
    LSTM_short.add(layers.LSTM(512,
                         return_sequences=False,
                         dropout=0.2
                        ))
    # add dense processing layer
    LSTM_short.add(layers.Dense(256, activation = 'tanh'))
    # add dense output layer
    LSTM_short.add(layers.Dense(long_nodes*lat_nodes, activation = 'sigmoid'))
    # compile LSTM model
    LSTM_short.compile(loss = 'mean_squared_error', optimizer="adam", metrics=['mse'])
    # return model
    return LSTM_short
