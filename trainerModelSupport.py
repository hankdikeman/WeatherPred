"""
Selection function for training/evaluation. When a specific model architecture is selected, it is passed into this function where the appropriate dataset is curated for further use
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
from LSTM_GenFuncs import *

def trainerModelSelect(model_num, x_nodes, y_nodes, day_num):
    if model_num == 1:
        return Gen_LSTM_Basic(x_nodes, y_nodes, day_num)
    if model_num == 2:
        return short_LSTM(x_nodes, y_nodes, day_num)
    if model_num == 3:
        return LSTM_BatchNorm(x_nodes, y_nodes, day_num)
    if model_num == 4:
        return LSTM_toConv(x_nodes, y_nodes, day_num)
    if model_num == 5:
        return LSTM_GRU(x_nodes, y_nodes, day_num)
    else:
        raise ValueError('invalid model selection')
    return 0
