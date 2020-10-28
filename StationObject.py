class Station:
    # Weather station class holds position and temp values recorded for a given station
    def __init__(self, temp, xcor, ycor):
        self.temp = temp
        self.lon = xcor
        self.lat = ycor
