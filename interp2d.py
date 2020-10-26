def interp2d(stations, temp_grid):
    from StationObject import Station
    
    # loop through all nodes on the temp_grid
    for i in range(shape(temp_grid)[0]):
        for j in range(shape(temp_grid)[1]):
            # Set denominator of IDW to 0
            sum_weights = 0
            for s in stations:
                # Calculate distance between station and point
                dx = temp_grid[i,j].xcor - s.xcor
                dy = temp_grid[i,j].ycor - s.ycor
                d = (dx**2 + dy**2)**0.5
                # Add station contribution to IDW
                temp_grid[i,j] += s.temp/(d**2)
                # Add dstance to distance weighting
                sum_weights += 1/(d**2)
            # Divude by sum of sum_weights
            temp_grid[i,j].temp = temp_grid[i,j].temp/sum_weights
        # Return IDW interpolated matrix
        return temp_grid
