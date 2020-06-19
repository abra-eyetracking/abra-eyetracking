import numpy as np



def linear_interpolate(data):
    """
    A function to linearly interpolate the data of a signal
    """
    nans = np.isnan(data)
    x = lambda z: z.nonzero()[0]
    data[nans] = np.interp(x(nans), x(~nans), data[~nans])
    return data
