import numpy as np

"""
Class to contain all of the trial data structures and epochs
"""

class Session:

    def __init__(self, trials, conditions = []):
        self.trials = trials
        self.conditions = conditions

    def summary(self):
        summary = {}

        # Pupil Data
        pupData = []
        for i in self.trials:
            for j in i.pupil_size:
                pupData.append(j)

        # Statistics and Shape of pupil_size across all session
        pupilMean = np.nanmean(pupData)
        summary['mean'] = pupilMean
        pupilVariance = np.nanvar(pupData)
        summary['variance'] == pupilVariance
        pupilStdDev = np.nanstd(pupData)
        summary['stdev'] == pupilStdDev
        pupilSize = len(pupData)
        summary['length'] == pupilSize
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

    def getValues(self):
        for i in self.trials:
            print(i.pupil_size)
        return
