import numpy as np
import random as rand
from . import trial
from . import session

"""
Class to contain all of the trial data structures and epochs
"""

def shuffle(Base):
    base = Base
    id = 0
    if isinstance(base, session.Session):
        id = 0
    elif isinstance(base, session.Epochs):
        id = 1
    else:
        raise ValueError("Only instances of the base class may be shuffled, Epochs or Session")
        return


    num_trial = len(base.data)
    instances = base.data
    conditions = base.conditions
    rand_idx = []

    while len(rand_idx) != num_trial:
        new = rand.randrange(0,num_trial)
        if new in rand_idx:
            continue
        else:
            rand_idx.append(new)

    new_instances = []
    new_conditions = []

    for i in rand_idx:
        instance = instances[i]
        new_instances.append(instance)
        cond = conditions[i]
        new_conditions.append(cond)

    if id == 0:
        return Session(np.array(new_instances), np.array(new_conditions))
    else:
        return Epochs(np.array(new_instances), np.array(new_conditions))

class Base:

    def __init__(self, data, conditions=None):
        self.data = data
        if conditions is not None:
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


    def select(self, indexes):
        new = self
        new_data = []
        new_cond = []
        for i in indexes:
            new_data.append(self.data[i])
            new_cond.append(self.conditions[i])
        new.data = new_data
        new.conditions = new_cond

        return new
        
class Session(Base):
    def __init__(self, trials, conditions=None):
        Base.__init__(self, trials, conditions)


class Epochs(Base):
    def __init__(self, epochs, conditions=None):
        Base.__init__(self, epochs, conditions)
