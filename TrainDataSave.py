import numpy as np
import pandas as pd
import datetime
from TOBS_US_weather_pull import *

# set start and end date of weather pull
# Started on 2000/01/01 format of date(year, month, day) no need for 09, just 9
# start V1 on 2000, 1, 1. Start V2 2000, 7, 30
startDate = datetime.date(2000, 7, 30)

day_jump = datetime.timedelta(days=1)
n_days = 720
csvname = "TrainData01012000"

for timejump in range(n_days):
    # pull data and assign to numpy array
    trainData = TOBS_US_weather_pull(startDate)
    date = np.array([startDate.year, startDate.month,
                     startDate.day]).reshape((1, 3))
    trainData = np.append(trainData, date, axis=1)
    maxtemp = np.amax(trainData)
    mintemp = np.amin(trainData)
    for i in range(50):
        print("max: " + str(maxtemp) + "  min: " + str(mintemp))
    # save to csv file
    with open('/Users/uvman/OneDrive/Desktop/WeatherData/' + csvname + '.csv', 'a+b') as f:
        np.savetxt(f, trainData, fmt='%d', newline=',', delimiter=',')
        f.write(b"\n")

    # add day to startDate
    startDate += day_jump
