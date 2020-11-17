#import packages and subfunctions
print('importing packages')
import tensorflow as tf
from tensorflow.keras import datasets, layers, models
import numpy as np
from ConvoNeuralNet_GenFuncs import *
from LSTM_GenFuncs import *
from NNDataFormat import *
import matplotlib.pyplot as plt

###
#   Generate Test and Train Data
###
print('preprocessing data')
# constants for data processing
filename = "../../Desktop/MNTrainData.csv"
x_nodes = 50
y_nodes = 50
day_num = 4
val_split = 0.8
# pull and format data from CSV
xdata,ydata = ConvLSTM2D_Format(filename, x_nodes, y_nodes, day_num)

##
#   Model preparation
##
print('generating model')
# generate model using generation function
CNNLSTM_model = Gen_CNN_LSTM(x_nodes, y_nodes, day_num, num_fil = 16)

##
#   Training/Visualization
##
batch_size = 128
epochs = 20
print('fitting model')
# run model on training data
history = CNNLSTM_model.fit(xdata, ydata, epochs = epochs, batch_size = batch_size, validation_split = 0.2, verbose = 1)

plt.plot(history.history['mse'], label='mse train')
plt.plot(history.history['val_mse'], label = 'mse validate')
plt.xlabel('Epoch')
plt.ylabel('Mean Squared Error')
plt.title('LSTM CNN MeanSquaredError')
plt.legend()
plt.ylim(0,0.2)
plt.show()
