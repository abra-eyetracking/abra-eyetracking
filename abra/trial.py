import numpy as np

"""
The trial class for individual trials within the 'data' data structure
"""

class trial:

    def __init__(self, timestamps, pupil_size):
        self.timestamps = timestamps
        self.pupil_size = pupil_size

    def summary(self):

        summary = {}

        # Pupil Data
        pupData = self.pupil_size

        # Statistics and Shape of pupil_size across all session
        pupilMean = np.nanmean(pupData)
        summary['mean'] = pupilMean
        pupilVariance = np.nanvar(pupData)
        summary['variance'] == pupilVariance
        pupilStdDev = np.nanstd(pupData)
        summary['stdev'] == pupilStdDev
        pupilSize = len(pupData)
        summary['lenght'] == pupilSize
        pupilMin = np.nanmin(pupData)
        summary['min'] == pupilMin
        pupilMax = np.nanmax(pupData)
        summary['max'] == pupilMax

        print("Session Pupil Mean: ", pupilMean, '\n'
                "Session Pupil Variance: ", pupilVariance, '\n'
                "Session Pupil Standard Deviation: ", pupilStdDev, '\n'
                "Session Pupil Data Length: ", pupilSize, '\n'
                "Session Minimum Pupil Size: ", pupilMin, '\n'
                "Session Maximum Pupil Size: ", pupilMax)

        return summary
