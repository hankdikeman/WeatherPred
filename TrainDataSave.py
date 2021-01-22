import numpy as np
import pandas as pd
import datetime
from TOBS_US_weather_pull import *
import os

# set start and end date of weather pull
# Started on 2000/01/01 format of date(year, month, day) no need for 09, just 9
# start V1 on 2000, 1, 1. Start V2 2000, 7, 30
# start V2 on 2000, 7, 30 Start V3 2001, 2, 25
# start V3 on 2001, 2, 25 Start V4 2001, 9, 18
# start V4 on 2001, 9, 18 Start V5 2002, 4, 15
startDate = datetime.date(2002, 12, 9)

day_jump = datetime.timedelta(days=1)
n_days = 720
csvname = os.path.join(os.getcwd(), 'TrainData12092002')

for timejump in range(n_days):
    print("start day: " + str(timejump))
    # pull data and assign to numpy array
    trainData = TOBS_US_weather_pull(startDate)
    maxtemp = np.amax(trainData)
    mintemp = np.amin(trainData)
    date = np.array([startDate.year, startDate.month,
                     startDate.day]).reshape((1, 3))
    trainData = np.append(trainData, date, axis=1)
    for i in range(50):
        print("max: " + str(maxtemp) + "  min: " + str(mintemp))
    # save to csv file
    with open(csvname + '.csv', 'a+b') as f:
        np.savetxt(f, trainData, fmt='%d', newline=',', delimiter=',')
        f.write(b"\n")

    # add day to startDate
    startDate += day_jump
