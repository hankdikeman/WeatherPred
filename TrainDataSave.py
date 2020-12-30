import numpy as np
import pandas as pd
import datetime
from TOBS_US_weather_pull import *

# set start and end date of weather pull
# Started on 2002/01/01 format of date(year, month, day) no need for 09, just 9
startDate = datetime.date(2004, 9, 16 )  # start V3 on 2002, 11, 15 to 2004, 9, 16, V2 good from 2002, 1, 1 to 2002, 11, 14
day_jump = datetime.timedelta(days = 1)
n_days = 720
csvname = "USTrainDataCurrent(11 to 26, 12, 2020)"

for timejump in range(n_days):
    # pull data and assign to numpy array
    trainData = TOBS_US_weather_pull(startDate)
    date = np.array([startDate.year, startDate.month, startDate.day]).reshape((1,3))
    trainData = np.append(trainData, date, axis=1)
    # save to csv file
    with open('/Users/patrickgibbons/Desktop/WeatherData/'+csvname+'.csv', 'a+b') as f:
        np.savetxt(f, trainData, fmt = '%d', newline = ',', delimiter = ',')
        f.write(b"\n")

    # add day to startDate
    startDate += day_jump
