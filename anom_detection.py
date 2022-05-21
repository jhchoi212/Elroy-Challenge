import numpy as np



def anomDetect(data_col, value):
    a = np.array(data_col)
    b = np.append([0], a)
    a = np.append(a, [0])

    diff = np.absolute(b-a)
    anom_val = np.argwhere(diff[1:len(diff)-1] > value/100)
    return anom_val
