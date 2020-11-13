import numpy as np
from NNDataFormat import *

filename = "../../Desktop/MNTrainData.csv"
x_nodes = 50
y_nodes = 50
day_num = 3

xtraindata,ytraindata = Convo_Format(filename, x_nodes, y_nodes, day_num)
