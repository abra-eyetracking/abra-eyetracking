import numpy as np

def linear_interpolate(data):
    nans = np.isnan(data)
    x = lambda z: z.nonzero()[0]
    data[nans] = np.interp(x(nans), x(~nans), data[~nans])
    return data
