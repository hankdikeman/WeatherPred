from LSTM_GenFuncs import *

def trainerModelSelect(model_num, x_nodes, y_nodes, day_num):
    switcher = {
        1: Gen_LSTM_Basic,
        2: short_LSTM,
        3: LSTM_BatchNorm,
        4: LSTM_toConv,
        5: LSTM_GRU
    }
    # Get the function from switcher dictionary
    func = switcher.get(model_num, lambda: "invalid selection")
    print(model_num + ' selected as generation function')
    # execute model generation function
    gen_model = func(x_nodes, y_nodes, day_num)
    return gen_model
