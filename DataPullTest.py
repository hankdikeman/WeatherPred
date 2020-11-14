import numpy as np
from NNDataFormat import *
import matplotlib.pyplot as plt

filename = "../../Desktop/MNTrainData.csv"
x_nodes = 50
y_nodes = 50
day_num = 4

xtraindata,ytraindata = LSTM_Format(filename, x_nodes, y_nodes, day_num)
print(np.shape(xtraindata))
print(np.shape(ytraindata))

#print(xtraindata)
#print(ytraindata)
print(str(np.amax(ytraindata)) + ' ' + str(np.amin(ytraindata)))
print(str(np.amax(ytraindata)*165-60) + ' ' + str(np.amin(ytraindata)*165-60))
print(str(np.mean(xtraindata)) + ' ' + str(np.mean(ytraindata*165-60)))

plt.plot(np.amin(ytraindata*165-60, axis = 1))
plt.show()
