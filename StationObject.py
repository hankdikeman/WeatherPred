"""
Simple station object for interpolation (IDW) and IDW constant optimization. Contains a temperature value and longitude/latitude coordinates
Author:     Henry Dikeman
Email:      dikem003@umn.edu
Date:       07/15/21
"""
class Station:
    # Weather station class holds position and temp values recorded for a given station
    def __init__(self, temp, xcor, ycor):
        self.temp = temp
        self.lon = xcor
        self.lat = ycor
