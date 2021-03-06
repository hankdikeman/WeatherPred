# import packages and subfunctions
from tensorflow.keras import models
import numpy as np
from trainerModelSupport import trainerModelSelect
from NNDataFormat import LSTM_Format2, nondimensionalize_input, redimensionalize_output
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
print('importing packages')

plt.style.use('seaborn-white')

###
#   Generate Test and Train Data
###
print('preprocessing data')
# constants for data processing
filename = "TrainDataCompiled_Mk2.csv"
x_nodes, y_nodes = (100, 175)
day_num = 7
days_prior = 1
# pull and format data from CSV
xdata, ydata = LSTM_Format2(filename, x_nodes, y_nodes, day_num, days_prior)

# user selection of model to be examined
print("Which neural net would you like to train?\nLSTM Basic: 1\nLSTM Short: 2\nBatchNormLSTM: 3\nLSTM w/ Conv: 4\nLSTM/GRU: 5")
print("\007")
model_num = int(input("\nPlease enter selection"))
# user selection of retrain or load model
print("\007")
load_or_train = input("\n\n(load) model or (retrain) model? ->")

##
#   Model preparation
##
if load_or_train == "retrain":
    print('generating model')
    # generate model using generation function
    LSTM_model = trainerModelSelect(model_num, x_nodes, y_nodes, day_num)
    LSTM_model.summary()

    ##
    #   Training/Visualization
    ##
    batch_size = 365
    epochs = 50
    print('fitting model')
    # run model on training data
    history = LSTM_model.fit(xdata, ydata, epochs=epochs,
                             batch_size=batch_size, validation_split=0.2, verbose=1)

    LSTM_model.save('./TrainedModels/' + str(model_num))
    print("\007")

    plt.plot(history.history['mse'], label='mse train')
    plt.plot(history.history['val_mse'], label='mse validate')
    plt.xlabel('Epoch')
    plt.ylabel('Mean Squared Error')
    plt.title('MeanSquaredError LSTM model #' + str(model_num))
    plt.legend()
    plt.ylim(0, 0.2)
    plt.show()
else:
    LSTM_model = models.load_model('./TrainedModels/' + str(model_num))
    print("\007")

calc_errors = input("\n\nCalculate All Errors (y) or select days (n)?")

if calc_errors == "y":
    # calculate all errors
    mseerrors = np.empty(shape=(np.shape(xdata)[0]))
    avgtemps = np.empty(shape=(np.shape(xdata)[0]))
    for ind_vis in range(np.shape(xdata)[0]):
        # pull inputs and predict
        inputs = xdata[ind_vis:ind_vis + 1, :, :]
        actual = np.reshape(ydata[ind_vis, :], newshape=(x_nodes, y_nodes))
        predicted = np.reshape(LSTM_model.predict(
            inputs)[0, :], newshape=(x_nodes, y_nodes))
        # gaussian filter
        actual = gaussian_filter(actual, sigma=2)
        predicted = gaussian_filter(predicted, sigma=2)
        # redimensionalize
        actual = redimensionalize_output(actual)
        # ((actual + 1) / 2 * 205) - 60
        predicted = redimensionalize_output(predicted)
        # ((predicted + 1) / 2 * 205) - 60
        mseerrors[ind_vis] = int(
            np.power(np.sum(np.square(actual - predicted)) / (x_nodes * y_nodes), 0.5))
        avgtemps[ind_vis] = np.mean(actual)

    print("\007")
    print(str(np.amax(mseerrors)) + ' ' + str(np.amin(mseerrors)))
    print(str(np.mean(mseerrors)))
    plt.hist(mseerrors, bins=25, range=(0, 25))
    plt.title('Distribution of (filtered) fit errors: LSTM model #' + str(model_num))
    plt.show()

    plt.plot(mseerrors, 'bo', zorder=50)
    plt.plot(avgtemps, 'ro', zorder=-50)
    plt.title('errors vs average day temps')
    plt.show()

while True:
    # select out input values
    ind_vis = int(input("index of selection"))
    inputs = xdata[ind_vis:ind_vis + 1, :, :]
    actual = np.reshape(ydata[ind_vis, :], newshape=(x_nodes, y_nodes))
    actual = gaussian_filter(actual, sigma=2)
    predicted = np.reshape(LSTM_model.predict(
        inputs)[0, :], newshape=(x_nodes, y_nodes))
    predicted = gaussian_filter(predicted, sigma=2)
    # reshape inputs
    inputs = np.reshape(inputs, newshape=(day_num, x_nodes, y_nodes))
    for i in range(day_num):
        inputs[i, :, :] = gaussian_filter(inputs[i, :, :], sigma=2)
    # redimensionalize values
    inputs = redimensionalize_output(inputs)
    # ((inputs + 1) / 2 * 205) - 60
    actual = redimensionalize_output(actual)
    # ((actual + 1) / 2 * 205) - 60
    predicted = redimensionalize_output(predicted)
    # ((predicted + 1) / 2 * 205) - 60
    avg_mse = int(np.sum(np.square(actual - predicted)) / (x_nodes * y_nodes))
    msevals = np.power(np.square(actual - predicted) /
                       (x_nodes * y_nodes), 0.5)
    # declare graph
    fig, axs = plt.subplots(3, 3)
    max_t = 130
    min_t = -20
    # plot inputs
    axs[0, 0].imshow(np.transpose(inputs[-7, :, :]),
                     cmap='gist_ncar', vmax=max_t, vmin=min_t)
    axs[0, 0].set_title('7 days prior')
    axs[0, 1].imshow(np.transpose(inputs[-6, :, :]),
                     cmap='gist_ncar', vmax=max_t, vmin=min_t)
    axs[0, 1].set_title('6 days prior')
    axs[0, 2].imshow(np.transpose(inputs[-5, :, :]),
                     cmap='gist_ncar', vmax=max_t, vmin=min_t)
    axs[0, 2].set_title('5 days prior')
    #
    axs[1, 0].imshow(np.transpose(inputs[-4, :, :]),
                     cmap='gist_ncar', vmax=max_t, vmin=min_t)
    axs[1, 0].set_title('4 days prior')
    axs[1, 1].imshow(np.transpose(inputs[-3, :, :]),
                     cmap='gist_ncar', vmax=max_t, vmin=min_t)
    axs[1, 1].set_title('3 days prior')
    axs[1, 2].imshow(np.transpose(inputs[-2, :, :]),
                     cmap='gist_ncar', vmax=max_t, vmin=min_t)
    axs[1, 2].set_title('2 days prior')
    axs[2, 0].imshow(np.transpose(inputs[-1, :, :]),
                     cmap='gist_ncar', vmax=max_t, vmin=min_t)
    axs[2, 0].set_title('1 days prior')
    # plot actual
    axs[2, 1].imshow(np.transpose(actual), cmap='gist_ncar',
                     vmax=max_t, vmin=min_t)
    axs[2, 1].set_title('actual temps')
    # plot predicted
    axs[2, 2].imshow(np.transpose(predicted),
                     cmap='gist_ncar', vmax=max_t, vmin=min_t)
    axs[2, 2].set_title('predicted temps, mse = ' + str(avg_mse))

    print("\007")
    plt.show(block=False)

    plt.show()
