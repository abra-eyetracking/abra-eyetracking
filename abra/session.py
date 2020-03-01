import numpy as np

"""
Class to contain all of the trial data structures and epochs
"""

class session:

    def __init__(self, trials, conditions = []):
        self.trials = trials
        self.conditions = conditions

    def summary(self):

        # Pupil Data
        pupData = []
        for i in self.trials:
            for j in i.pupil_size:
                pupData.append(j)
                
        # Statistics and Shape of pupil_size across all session
        pupilMean = np.nanmean(pupData)
        pupilVariance = np.nanvar(pupData)
        pupilStdDev = np.nanstd(pupData)
        pupilSize = len(pupData)
        pupilMin = np.nanmin(pupData)
        pupilMax = np.nanmax(pupData)

        print("Session Pupil Mean: ", pupilMean, '\n'
                "Session Pupil Variance: ", pupilVariance, '\n'
                "Session Pupil Standard Deviation: ", pupilStdDev, '\n'
                "Session Pupil Data Length: ", pupilSize, '\n'
                "Session Minimum Pupil Size: ", pupilMin, '\n'
                "Session Maximum Pupil Size: ", pupilMax)
        return

    def getValues(self):
        for i in self.trials:
            print(i.pupil_size)
        return
