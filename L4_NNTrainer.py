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
xdata,ydata = LSTM_Format(filename, x_nodes, y_nodes, day_num)

##
#   Model preparation
##
print('generating model')
# generate model using generation function
LSTM_model = short_LSTM(x_nodes, y_nodes, day_num)

##
#   Training/Visualization
##
batch_size = 128
epochs = 25
print('fitting model')
# run model on training data
history = LSTM_model.fit(xdata, ydata, epochs = epochs, batch_size = batch_size, validation_split = 0.2, verbose = 1)

plt.plot(history.history['mse'], label='mse train')
plt.plot(history.history['val_mse'], label = 'mse validate')
plt.xlabel('Epoch')
plt.ylabel('Mean Squared Error')
plt.title('Short LSTM MeanSquaredError')
plt.legend()
plt.ylim(0,0.2)
plt.show()

while True:
    # select out input values
    ind_vis = int(input("index of selection"))
    inputs = xdata[ind_vis:ind_vis+1,:,:]
    actual = np.reshape(ydata[ind_vis,:], newshape = (x_nodes,y_nodes))
    predicted = np.reshape(LSTM_model.predict(inputs)[0,:], newshape = (x_nodes,y_nodes))
    # reshape inputs
    inputs = np.reshape(inputs, newshape = (day_num,x_nodes,y_nodes))

    # redimensionalize values
    inputs = ((inputs+1)/2*165)-60
    actual = ((actual+1)/2*165)-60
    predicted = ((predicted+1)/2*165)-60
    avg_mse = int(np.sum(np.square(actual - predicted))/(x_nodes*y_nodes))
    # declare graph
    fig,axs = plt.subplots(3,2)
    max_t = int(np.amax(inputs))
    min_t = int(np.amin(inputs))
    # plot inputs
    axs[0,0].imshow(inputs[0,:,:], cmap = 'magma', vmax = max_t, vmin = min_t)
    axs[0,0].set_title('4 days prior')
    axs[0,1].imshow(inputs[1,:,:], cmap = 'magma', vmax = max_t, vmin = min_t)
    axs[0,1].set_title('3 days prior')
    axs[1,0].imshow(inputs[2,:,:], cmap = 'magma', vmax = max_t, vmin = min_t)
    axs[1,0].set_title('2 days prior')
    axs[1,1].imshow(inputs[3,:,:], cmap = 'magma', vmax = max_t, vmin = min_t)
    axs[1,1].set_title('1 days prior')
    # plot actual
    axs[2,0].imshow(actual, cmap = 'magma', vmax = max_t, vmin = min_t)
    axs[2,0].set_title('actual temps')
    # plot predicted
    axs[2,1].imshow(predicted, cmap = 'magma', vmax = max_t, vmin = min_t)
    axs[2,1].set_title('predicted temps, mse = '+str(avg_mse))

    plt.show()
