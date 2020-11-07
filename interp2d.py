from StationObject import Station
import numpy as np

def interp2d(stations, temp_grid, xcords, ycords, p):
    # assign start and end variables
    xstart,xend = xcords
    ystart,yend = ycords
    # retreive temp grid dimensions
    xrange = np.shape(temp_grid)[0]
    yrange = np.shape(temp_grid)[1]
    # loop through all nodes on the temp_grid
    for i in range(xrange):
        for j in range(yrange):
            # calculate position of temperature nodes
            xpos = xstart + (i/(xrange-1)) * (xend - xstart)
            ypos = ystart + (j/(yrange-1)) * (yend - ystart)
            # Set denominator of IDW to 0
            node_temp = 0
            sum_weights = 0
            for s in stations:
                # Calculate distance between station and point
                dx = xpos - s.lon
                dy = ypos - s.lat
                d = (dx**2 + dy**2)**0.5
                # Add station contribution to IDW
                node_temp += s.temp * (1/(d**p))
                # Add dstance to distance weighting
                sum_weights += 1/(d**p)
            # Divude by sum of sum_weights
            temp_grid[i,j] = int(node_temp/sum_weights)
    # Return IDW interpolated matrix
    return temp_grid
