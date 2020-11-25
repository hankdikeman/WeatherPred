import numpy as np
import pandas as pd
import datetime
from TOBS_US_weather_pull import *

# set start and end date of weather pull
startDate = datetime.date(2000, 12, 21)
day_jump = datetime.timedelta(days = 1)
n_days = 730
<<<<<<< HEAD
csvname = "USTrainData"
=======
csvname = "TempTrainData"
>>>>>>> 5a23954007104f3f7fb4f230710da53c285389ca

for timejump in range(n_days):
    # set date range
    dateRange = (startDate, startDate)
    # pull data and assign to numpy array
    trainData = TOBS_US_weather_pull(dateRange)
    # save to csv file
<<<<<<< HEAD
    with open('~/Desktop/WeatherData/'+csvname+'.csv', 'ab') as f:
        np.savetxt(f, trainData, fmt = '%d', newline = ',', delimiter = ',')
    
=======
    with open('../../Desktop/'+csvname+'.csv', 'ab') as f:
        # date of weather data
        np.savetxt(f, trainData, fmt = '%d', newline = ", ", delimiter = ',')
>>>>>>> 5a23954007104f3f7fb4f230710da53c285389ca

    print("saved to file with name " + csvname)
    # add day to startDate
    startDate += day_jump
