import numpy as np

"""
The trial class for individual trials within the 'data' data structure
"""

class Trial:

    def __init__(self, timestamps, pupil_size, movement_X = [], movement_y = [], event_L = [], event_R = []):
        self.timestamps = timestamps
        self.pupil_size = pupil_size
        self.movement_X = movement_X
        self.movement_y = movement_y
        self.event_L = event_L
        self.event_R = event_R
        #TODO: add movement size

    def summary(self):

        summary = {}

        # Pupil Data
        pup_data = self.pupil_size

        # Statistics and Shape of pupil_size across all session
        pupil_mean = np.nanmean(pup_data)
        summary['mean'] = pupil_mean
        pupil_variance = np.nanvar(pup_data)
        summary['variance'] = pupil_variance
        pupil_stddev = np.nanstd(pup_data)
        summary['stdev'] = pupil_stddev
        pupil_size = len(pup_data)
        summary['length'] = pupil_size
        pupil_min = np.nanmin(pup_data)
        summary['min'] = pupil_min
        pupil_max = np.nanmax(pup_data)
        summary['max'] = pupil_max

        print("Session Pupil Mean: ", pupil_mean, '\n'
                "Session Pupil Variance: ", pupil_variance, '\n'
                "Session Pupil Standard Deviation: ", pupil_stddev, '\n'
                "Session Pupil Data Length: ", pupil_size, '\n'
                "Session Minimum Pupil Size: ", pupil_min, '\n'
                "Session Maximum Pupil Size: ", pupil_max)

        return summary
