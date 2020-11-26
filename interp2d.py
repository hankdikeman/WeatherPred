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
                if abs(dx) < 4:
                    dy = ypos - s.lat
                    if abs(dy) < 1.5:
                        d = (dx**2 + dy**2)**0.5
                        # check if distance = 0, if so set to station temp
                        if d == 0:
                            node_temp = s.temp
                            sum_weights = 1
                            break
                        # perform operation normally otherwise
                        else:
                            node_temp += s.temp * (1/(d**p))
                            # Add distance to distance weighting
                            sum_weights += 1/(d**p)
            # Divide by sum of sum_weights
            if sum_weights == 0:
                temp_grid[i,j] = 0
            else:
                temp_grid[i,j] = node_temp/sum_weights
    # Return IDW interpolated matrix
    return temp_grid
