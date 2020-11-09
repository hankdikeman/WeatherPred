import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

# first LSTM model
def Gen_LSTM_Basic(long_nodes, lat_nodes, day_num):
    LSTM_model = Sequential()
    # LSTM 1: return sequences because we have more LSTM layers
    LSTM_model.add(LSTM(256, return_sequences=True, input_shape = (day_num,long_nodes*lat_nodes) ))
    LSTM_model.add(Dropout(0.2))
    # LSTM 2: return sequences because we have more LSTM layers
    LSTM_model.add(LSTM(256, return_sequences=True))
    LSTM_model.add(Dropout(0.2))
    # LSTM 3: return sequences because we have more LSTM layers
    LSTM_model.add(LSTM(256, return_sequences=True))
    LSTM_model.add(Dropout(0.2))
    # LSTM 4: no return sequences because we have dense next
    LSTM_model.add(LSTM(256))
    LSTM_model.add(Dropout(0.2))
    # Dense output layer, 1 for now
    LSTM_model.add(Dense(128, activation='relu'))
    LSTM_model.add(Dense(lat_nodes*long_nodes, activation='sigmoid'))

    LSTM_model.compile(optimizer='adam', loss='mean_squared_error',metrics=['accuracy'])

    return LSTM_model
####
#   LSTM number 2
#   insert model generation function here
####
