import numpy as np

"""
The trial class for individual trials within the 'data' data structure
"""

class trial:

    def __init__(self, timestamps, pupil_size):
        self.timestamps = timestamps
        self.pupil_size = pupil_size

    def summary(self):

        # Pupil Data
        pupData = self.pupil_size

        # Statistics and Shape of pupil_size across trials
        pupilMean = np.nanmean(pupData)
        pupilVariance = np.nanvar(pupData)
        pupilStdDev = np.nanstd(pupData)
        pupilSize = len(pupData)
        pupilMin = np.nanmin(pupData)
        pupilMax = np.nanmax(pupData)

        print("Trial Pupil Mean: ", pupilMean, '\n'
                "Trial Pupil Variance: ", pupilVariance, '\n'
                "Trial Pupil Standard Deviation: ", pupilStdDev, '\n'
                "Trial Pupil Data Length: ", pupilSize, '\n'
                "Trial Minimum Pupil Size: ", pupilMin, '\n'
                "Trial Maximum Pupil Size: ", pupilMax)

        return
