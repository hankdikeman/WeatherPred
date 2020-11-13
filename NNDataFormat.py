import numpy as np

def Convo_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, dtype = float, delimiter = ',', names = False)
    # get shape of raw data
    x_len,y_len = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_xdata = np.empty(shape = (y_len-day_num, x_nodes, y_nodes, day_num))
    # loop through all days minus day_num allocation
    for ind in range(y_len-day_num):
        # reshape "day_num" section to shape required for x output
        sample = np.reshape(rawdata[ind:ind+day_num,:], newshape = (x_nodes, y_nodes, day_num))
        # store x input values in formatted data
        formatted_xdata[ind,:,:,:] = sample
    # take y data from raw data array
    formatted_ydata = rawdata[day_num:,:]
    # reshape
    return formatted_xdata,formatted_ydata

def ConvLSTM2D_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, dtype = float, delimiter = ',', names = False)
    # get shape of raw data
    x_len,y_len = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_xdata = np.empty(shape = (y_len-day_num, day_num, x_nodes, y_nodes, 1))
    # loop through all days minus day_num allocation
    for ind in range(y_len-day_num):
        # reshape "day_num" section to shape required for x output
        sample = np.reshape(rawdata[ind:ind+day_num,:], newshape = (day_num, x_nodes, y_nodes, 1))
        # store x input values in formatted data
        formatted_xdata[ind,:,:,:,:] = sample
    # take y data from raw data array
    formatted_ydata = rawdata[day_num:,:]
    return formatted_xdata,formatted_ydata

def LSTM_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, dtype = float, delimiter = ',', names = False)
    # get shape of raw data
    x_len,y_len = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_data = np.empty(shape = (y_len-day_num, day_num, x_nodes*y_nodes))
    # loop through all days minus day_num allocation
    for ind in range(y_len-day_num):
        # reshape "day_num" section to shape required for x output
        sample = np.reshape(rawdata[ind:ind+day_num,:], newshape = (day_num, x_nodes*y_nodes))
        # store x input values in formatted data
        formatted_xdata[ind,:,:] = sample
    # take y data from raw data array
    formatted_ydata = rawdata[day_num:,:]
    return formatted_xdata,formatted_ydata
