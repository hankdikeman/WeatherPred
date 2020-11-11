import pandas as pd
import numpy as np
from StationObject import Station

def PvalOpt_FindIndex(rpoint, horz_dims, vert_dims, xcords, ycords):
    horz_seq = np.arange(xcords[0], xcords[1], (xcords[1]-xcords[0])/horz_dims)
    vert_seq = np.arange(ycords[0], ycords[1], (ycords[1]-ycords[0])/vert_dims)

    horz_dif = 100
    x_index = None
    for i in range(len(horz_seq)):
        dif = abs(horz_seq[i] - rpoint.lon)
        if (dif < horz_dif):
            x_index = i
            horz_dif = dif


    vert_dif = 100
    y_index = None
    for j in range(len(vert_seq)):
        dif = abs(vert_seq[i] - rpoint.lat)
        if (dif < vert_dif):
            y_index = i
            vert_dif = dif

    return((x_index, y_index))
