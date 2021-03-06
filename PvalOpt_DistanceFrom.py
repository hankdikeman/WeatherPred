import math
def closest_distance(point, data):
    min_dist = 1000
    for i in data:
        lon_dist = abs(point.lon - i.lon)
        lat_dist = abs(point.lat - i.lat)
        dist = math.sqrt(lon_dist**2 + lat_dist**2)

        if (dist < min_dist):
            min_dist = dist

    return (min_dist)
