import numpy as np
from MNWeatherPull import *

dateRange = ([1998,10,20],[1998,10,30])

tempvals = PullMNWeather(dateRange)

print(tempvals[10:40,:])
print(np.shape(tempvals))
