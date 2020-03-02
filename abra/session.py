import numpy as np
import random as rand
from . import trial
from . import session

def shuffle(session):
    sess = session
    num_trial = len(sess.trials)
    trials = sess.trials
    conditions = sess.conditions
    rand_idx = []

    while len(rand_idx) != num_trial:
        new = rand.randrange(0,num_trial)
        if new in rand_idx:
            continue
        else:
            rand_idx.append(new)

    new_trials = []
    new_conditions = []
    for i in rand_idx:
        trial = trials[i]
        new_trials.append(trial)
        cond = conditions[i]
        new_conditions.append(cond)

    return Session(np.array(new_trials), np.array(new_conditions))


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
        pup_data = []
        for i in self.trials:
            for j in i.pupil_size:
                pup_data.append(j)

        # Statistics and Shape of pupil_size across all session
        pupil_mean = np.nanmean(pupil_mean)
        summary['mean'] = pupil_mean
        pupil_variance = np.nanvar(pupil_mean)
        summary['variance'] = pupil_variance
        pupil_stddev = np.nanstd(pupil_mean)
        summary['stdev'] = pupil_stddev
        pupil_size = len(pupil_mean)
        summary['length'] = pupil_size
        pupil_min = np.nanmin(pupil_mean)
        summary['min'] = pupil_min
        pupil_max = np.nanmax(pupil_mean)
        summary['max'] = pupil_max

        print("Session Pupil Mean: ", pupil_mean, '\n'
                "Session Pupil Variance: ", pupil_variance, '\n'
                "Session Pupil Standard Deviation: ", pupil_stddev, '\n'
                "Session Pupil Data Length: ", pupil_size, '\n'
                "Session Minimum Pupil Size: ", pupil_min, '\n'
                "Session Maximum Pupil Size: ", pupil_max)

        return summary

    def get_values(self):
        for i in self.trials:
            print(i.pupil_size)
        return
