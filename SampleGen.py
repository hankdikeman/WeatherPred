import numpy as np

# Take in a matrix of weatherData in standard form and return n_samp samples
def setSample(weatherData, n_samp, n_prior, col_target):
    # save number of sample days in weatherData
    n_days = np.shape(weatherData)[0]
    # if weatherData is equal to number of desired samples, return them all
    if(n_days <= n_samp-n_prior):
        day_samp = np.random.choice(n_days-n_prior, size = n_days - nprior, replace = False)
        x_samp = [day_samp,:]
        y_samp = [day_samp+nprior,col_target]
    # else only the amount of requested samples should be sent
    else:
        day_samp = np.random.choice(n_samp, size = n_days - nprior, replace = False)
        x_samp = [day_samp,:]
        y_samp = [day_samp+nprior,col_target]
    # return tuple of x and y values
    return (x_samp, y_samp)
