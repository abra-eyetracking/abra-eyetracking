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

class Base:

    def __init__(self, data, conditions=None):
        self.data = data
        if conditions:
            self.conditions = conditions
        else:
            self.conditions = np.zeros(len(self.data))

    def summary(self):
        summary = {}

        # Pupil Data
        pup_data = []
        for i in self.data:
            for j in i.pupil_size:
                pup_data.append(j)

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

    def get_values(self):
        tmp_ls = []
        for i in self.data:
            tmp_ls.append(i.pupil_size)
        return np.array(tmp_ls)

    def get_timestamps(self):
        tmp_ls = []
        for i in self.data:
            tmp_ls.append(i.timestamps)
        return np.array(tmp_ls)


class Session(Base):
    def __init__(self, trials, conditions=None):
        Base.__init__(self, trials, conditions)


class Epochs(Base):
    def __init__(self, epochs, conditions=None):
        Base.__init__(self, epochs, conditions)
