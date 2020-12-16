import numpy as np

def Convo_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, delimiter = ',')[:,:-1]
    # get shape of raw data
    rows,cols = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_xdata = np.zeros(shape = (rows-day_num, x_nodes, y_nodes, day_num))
    # loop through all days minus day_num allocation
    print(rawdata[5:5+day_num,:].shape)
    for ind in range(rows-day_num):
        # reshape "day_num" section to shape required for x output
        for dayind in range(day_num):
            formatted_xdata[ind,:,:,dayind] = np.reshape(rawdata[ind+dayind,:], newshape = (x_nodes, y_nodes))
    # take y data from raw data array
    print(formatted_xdata.shape)
    formatted_xdata = ((formatted_xdata+60)/165)*2-1
    formatted_ydata = ((rawdata[day_num:,:]+60)/165)*2-1
    # reshape
    return formatted_xdata,formatted_ydata

def ConvLSTM2D_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, delimiter = ',')[:,:-1]
    # get shape of raw data
    rows,cols = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_xdata = np.empty(shape = (rows-day_num, day_num, x_nodes, y_nodes, 1))
    # loop through all days minus day_num allocation
    for ind in range(rows-day_num):
        # reshape "day_num" section to shape required for x output
        for dayind in range(day_num):
            formatted_xdata[:,dayind,:,:,:] = np.reshape(rawdata[ind+dayind,:], newshape = (x_nodes, y_nodes))
    # take y data from raw data array
    formatted_xdata = ((formatted_xdata+60)/165)*2-1
    formatted_ydata = ((rawdata[day_num:,:]+60)/165)*2-1
    return formatted_xdata,formatted_ydata

def LSTM_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, delimiter = ',')[:,:-1]
    # get shape of raw data
    rows,cols = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_xdata = np.empty(shape = (rows-day_num, day_num, x_nodes*y_nodes))
    # loop through all days minus day_num allocation
    for ind in range(rows-day_num):
        # reshape "day_num" section to shape required for x output
        sample = np.reshape(rawdata[ind:ind+day_num,:], newshape = (1, day_num, x_nodes*y_nodes))
        # store x input values in formatted data
        formatted_xdata[ind,:,:] = sample
    # take y data from raw data array
    formatted_xdata = ((formatted_xdata+60)/165)*2-1
    formatted_ydata = ((rawdata[day_num:,:]+60)/165)*2-1
    return formatted_xdata,formatted_ydata

def LSTM_Format2(filename, x_nodes, y_nodes, day_num, day_prior):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, delimiter = ',')[:,:-4]
    print(np.shape(rawdata))
    print(np.amax(rawdata))
    print(np.amin(rawdata))
    print(rawdata[:,0])
    flatdata = np.sort(rawdata, axis = None)
    print(flatdata[-10:-1])
    # get shape of raw data
    rows,cols = np.shape(rawdata)
    # sample index
    sample_ind = rows - day_num - day_prior + 1
    # generate empty list of CNN format
    formatted_xdata = np.empty(shape = (sample_ind, day_num, x_nodes*y_nodes))
    # loop through all days minus day_num allocation
    for ind in range(sample_ind):
        # reshape "day_num" section to shape required for x output
        sample = np.reshape(rawdata[ind:ind+day_num,:], newshape = (1, day_num, x_nodes*y_nodes))
        # store x input values in formatted data
        formatted_xdata[ind,:,:] = sample
    # take y data from raw data array
    formatted_xdata = ((formatted_xdata+60)/165)*2-1
    formatted_ydata = ((rawdata[day_num+day_prior-1:,:]+60)/165)*2-1
    return formatted_xdata,formatted_ydata
