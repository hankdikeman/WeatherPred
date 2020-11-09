import numpy as np
import pandas as pd
import datetime
from MNWeatherPull import *

# set start and end date of weather pull
startDate = datetime.date(2018, 12, 21)
day_jump = datetime.timedelta(days = 1)
n_days = 730
csvname = "MNTrainData"

for timejump in range(n_days):
    # set date range
    dateRange = (startDate, startDate)
    # pull data and assign to numpy array
    trainData = PullMNWeather(dateRange)
    # save to csv file
    with open('../../Desktop/'+csvname+'.csv', 'ab') as f:
        np.savetxt(f, trainData, fmt = '%d', newline = ", ", delimiter = ',')
        f.write(b"\n")

    print("saved to file with name " + csvname)
    # add day to startDate
    startDate += day_jump
