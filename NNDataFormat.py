"""
This file loads and formats data in the proper format for each neural net architecture used. Receives a filename, dimensions of data, and number of days in advance needed for each training iteration
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
import numpy as np

MAX_TEMP = 140
MIN_TEMP = -60


# redimensionalize output of model
def nondimensionalize_input(output_array):
    return np.interp(output_array, (MIN_TEMP, MAX_TEMP), (-1, +1))


# nondimensionalize input of model
def redimensionalize_output(input_array):
    return np.interp(input_array, (-1, +1), (MIN_TEMP, MAX_TEMP))


def Convo_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, delimiter=',')[:, :-1]
    # get shape of raw data
    rows, cols = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_xdata = np.zeros(
        shape=(rows - day_num, x_nodes, y_nodes, day_num))
    # loop through all days minus day_num allocation
    for ind in range(rows - day_num):
        # reshape "day_num" section to shape required for x output
        for dayind in range(day_num):
            formatted_xdata[ind, :, :, dayind] = np.reshape(
                rawdata[ind + dayind, :], newshape=(x_nodes, y_nodes))
    # take y data from raw data array
    formatted_xdata = ((formatted_xdata + 60) / 165) * 2 - 1
    formatted_ydata = ((rawdata[day_num:, :] + 60) / 165) * 2 - 1
    # reshape
    return formatted_xdata, formatted_ydata


def ConvLSTM2D_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, delimiter=',')[:, :-1]
    # get shape of raw data
    rows, cols = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_xdata = np.empty(
        shape=(rows - day_num, day_num, x_nodes, y_nodes, 1))
    # loop through all days minus day_num allocation
    for ind in range(rows - day_num):
        # reshape "day_num" section to shape required for x output
        for dayind in range(day_num):
            formatted_xdata[:, dayind, :, :, :] = np.reshape(
                rawdata[ind + dayind, :], newshape=(x_nodes, y_nodes))
    # take y data from raw data array
    formatted_xdata = ((formatted_xdata + 60) / 165) * 2 - 1
    formatted_ydata = ((rawdata[day_num:, :] + 60) / 165) * 2 - 1
    return formatted_xdata, formatted_ydata


def LSTM_Format(filename, x_nodes, y_nodes, day_num):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, delimiter=',')[:, :-1]
    # get shape of raw data
    rows, cols = np.shape(rawdata)
    # generate empty list of CNN format
    formatted_xdata = np.empty(
        shape=(rows - day_num, day_num, x_nodes * y_nodes))
    # loop through all days minus day_num allocation
    for ind in range(rows - day_num):
        # reshape "day_num" section to shape required for x output
        sample = np.reshape(
            rawdata[ind:ind + day_num, :], newshape=(1, day_num, x_nodes * y_nodes))
        # store x input values in formatted data
        formatted_xdata[ind, :, :] = sample
    # take y data from raw data array
    formatted_xdata = ((formatted_xdata + 60) / 165) * 2 - 1
    formatted_ydata = ((rawdata[day_num:, :] + 60) / 165) * 2 - 1
    return formatted_xdata, formatted_ydata


def LSTM_Format2(filename, x_nodes, y_nodes, day_num, day_prior):
    # import temp data from csv
    rawdata = np.genfromtxt(filename, delimiter=',')[:, :-3]
    # get shape of raw data
    rows, cols = np.shape(rawdata)
    # sample index
    sample_ind = rows - day_num - day_prior + 1
    # generate empty list of CNN format
    formatted_xdata = np.empty(shape=(sample_ind, day_num, x_nodes * y_nodes))
    # loop through all days minus day_num allocation
    for ind in range(sample_ind):
        # reshape "day_num" section to shape required for x output
        sample = np.reshape(
            rawdata[ind:ind + day_num, :], newshape=(1, day_num, x_nodes * y_nodes))
        # store x input values in formatted data
        formatted_xdata[ind, :, :] = sample
    # take y data from raw data array
    formatted_xdata = nondimensionalize_input(formatted_xdata)
    # ((formatted_xdata + 60) / 205) * 2 - 1
    formatted_ydata = nondimensionalize_input(
        rawdata[day_num + day_prior - 1:, :])
    # ((rawdata[day_num + day_prior - 1:, :] + 60) / 205) * 2 - 1
    return formatted_xdata, formatted_ydata
