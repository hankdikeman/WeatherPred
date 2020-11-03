import numpy as np

# Take in a matrix of weatherData in standard form and return sample_size samples
def setSample(weatherData, sample_size, days_before):
    # save number of sample days in weatherData
    num_days = np.shape(weatherData)[0]
    # if weatherData is equal or smaller to number of desired samples, return them all
    if(num_days <= sample_size-days_before):
        rand_days = np.random.choice(num_days-days_before, size = num_days - nprior, replace = False)
        x_samp = weatherData[rand_days,:]
        for day_added in range(start = 1, stop = nprior):
            xsamp = vstack(xsamp, weatherData[rand_days+day_added,:])
        y_samp = weatherData[rand_days+nprior,:]
    # else only the amount of requested samples should be sent
    else:
        rand_days = np.random.choice(sample_size, size = num_days - nprior, replace = False)
        for day_added in range(start = 1, stop = nprior):
            xsamp = vstack(xsamp, weatherData[rand_days+day_added,:])
        y_samp = weatherData[rand_days+nprior,:]
    # return tuple of x and y values
    return (x_samp, y_samp)
