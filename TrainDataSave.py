import numpy as np
import pandas as pd
import datetime
from TOBS_US_weather_pull import *

# set start and end date of weather pull
# Started on 2002/01/01 format of date(year, month, day) no need for 09, just 9
<<<<<<< HEAD
startDate = datetime.date(2008, 1, 21 )  # start V3 on 2002, 11, 15 to 2004, 9, 16, V2 good from 2002, 1, 1 to 2002, 11, 14
=======
# start V3 on 2002, 11, 15 to 2004, 9, 16, V2 good from 2002, 1, 1 to 2002, 11, 14
startDate = datetime.date(2008, 1, 6)
>>>>>>> 7f854b6bb33fefd82c24b68e8d424842a730c917
# Start V4 on 2004, 9, 16 to 2005, 3, 16 to 2005, 4, 1. Start V5 on 2005, 4, 2 to 2005, 4, 16
# Start V6 on 2005, 4, 17 to 2005, 5, 31. Start V7 on 2005, 6, 1 to 2005,11, 13
# Start V8 on 2005, 11, 14 to 2005, 12, 28. Start V9 on 2005, 12, 29 to 2006, 6, 12
# Start V10 on 2006, 6, 13 to 2006, 8, 8. Start V11 on 2006, 8, 9 to 2006, 9, 13
# Start V11 on 2006, 9, 14 to 2006, 12, 5. Start V12 on 2006, 12, 5 to 2007, 2, 3.
# Start V13 on 2007, 2, 4 to 2007, 3, 3. # Start V14 on 2007, 3, 4 to 2007, 4, 23
# Start V15 on 2007, 4, 24 to 2007, 11, 21. #V16 to 2008, 1, 5.

day_jump = datetime.timedelta(days=1)
n_days = 720
csvname = "USTrainDataCurrent(11, 22, 2020 to )"

for timejump in range(n_days):
    # pull data and assign to numpy array
    trainData = TOBS_US_weather_pull(startDate)
    date = np.array([startDate.year, startDate.month,
                     startDate.day]).reshape((1, 3))
    trainData = np.append(trainData, date, axis=1)
    maxtemp = np.amax(trainData)
    mintemp = np.amin(trainData)
    for i in range(50):
        print("min: " + str(maxtemp) + "  max: " + str(mintemp))
    # save to csv file
    with open('/Users/uvman/OneDrive/Desktop/WeatherData/' + csvname + '.csv', 'a+b') as f:
        np.savetxt(f, trainData, fmt='%d', newline=',', delimiter=',')
        f.write(b"\n")

    # add day to startDate
    startDate += day_jump
