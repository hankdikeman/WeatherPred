import numpy as np
import pandas as pd
from MNWeatherPull import *

# set start and end date of weather pull
startDate = [1998,8,20]
endDate = [2008,8,30]
dateRange = (startDate,endDate)

# pull data and assign to numpy array
trainData = PullMNWeather(dateRange)
print(trainData)

# save to csv file
pd.DataFrame(trainData).to_csv("../../Desktop/MNTrainData.csv")
