import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image
import matplotlib.image as mpimg
import random as rand
from . import trial
from . import session
import copy



def shuffle(Base):

    """
    Randomly Shuffles Trials in Epoch and Sessions
    """

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

    """
    Base Class for Session and Epoch
    """
    def __init__(self, data, sample_rate, conditions=None):
        self.data = data
        self.sample_rate = sample_rate
        if conditions is not None:
            self.conditions = conditions
        else:
            self.conditions = np.zeros(len(self.data))



    def summary(self, verbose = False):

        """
        summary: Dictionary of summary statistic for pupil size
            > mean: pupil mean
            > variance: pupil variance
            > stdev: pupil standard deviation
            > length: pupil size
            > min: pupil minimum
            > maximum: pupil maximum
        """

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

        if verbose:
            print("Session Pupil Mean: ", pupil_mean, '\n'
                    "Session Pupil Variance: ", pupil_variance, '\n'
                    "Session Pupil Standard Deviation: ", pupil_stddev, '\n'
                    "Session Pupil Data Length: ", pupil_size, '\n'
                    "Session Minimum Pupil Size: ", pupil_min, '\n'
                    "Session Maximum Pupil Size: ", pupil_max)

        return summary



    def get_trial(self, trial_num):

        """
        Return Specified Trial
        > 1 == index 0 for trial list
        """

        trial = self.data[trial_num-1]
        return trial



    def get_pupil(self):

        """
        Returns Numpy Array Of Trials Containing Pupil Sizes
        """

        tmp_ls = []
        for i in self.data:
            tmp_ls.append(i.pupil_size)
        return np.array(tmp_ls)



    def get_movement(self):

        """
        Returns Numpy Array Of Trials Containing Movements
            > index 0: x-coordinates
            > index 1: y-coordinates
        """

        move_list = [[],[]]
        for i in self.data:
            move_list[0].append(i.movement_X)
            move_list[1].append(i.movement_y)
        return np.array(move_list)

    def get_timestamps(self):

        """
        Returns Numpy Array Of Trials Containing Timestamps
        """

        tmp_ls = []
        for i in self.data:
            tmp_ls.append(i.timestamps)
        return np.array(tmp_ls)



    def get_fixation(self):

        """
        Returns Numpy Array Of Trials Containing
         x And y Fixations Coordinates
         ie. Trial 1 x-coordinate
         > fixation[0][0][0]
         ie. Trial 2 y-coordinate
         > fixation[1][0][1]
        """

        tmp_ls = np.array(self.get_timestamps())
        movement_list = self.get_movement()
        fix = [[] for _ in range(tmp_ls.shape[0])]
        fix_list = [[] for _ in range(tmp_ls.shape[0])]
        RL = ''

        count = 0
        if(len(self.data[0].event_L) > 0):
            RL = 'L'
        elif(len(self.data[0].event_R ) > 0):
            RL = 'R'
        else:
            print('NO FIXATION FOUND')
            pass
        if(RL == 'L'):
            for i in tmp_ls:
                for j in self.data:
                    if(j.event_L[1] in i):
                        fix[count].append([j.event_L[0],j.event_L[1]])
                count += 1
        elif(RL == 'R'):
            for i in tmp_ls:
                index = 0
                for h in self.data:
                    for j in h.event_R:
                        if(j[1] in i):
                            fix[count].append([j[0],j[1]])
                count += 1

        for index in range(len(tmp_ls)):
            movements = [[],[]]
            in_fix = False
            for fix_index in fix[index]:
                for time_index in range(len(tmp_ls[index])):
                    if(fix_index[0] == tmp_ls[index][time_index]):
                        in_fix = True

                    elif(fix_index[1] == tmp_ls[index][time_index]):
                        in_fix = False
                        movements[0].append(movement_list[0][index][time_index])
                        movements[1].append(movement_list[1][index][time_index])
                        fix_list[index].append(movements)
                        movements = [[],[]]

                    if(in_fix):
                        movements[0].append(movement_list[0][index][time_index])
                        movements[1].append(movement_list[1][index][time_index])
            fix_list[index].append(movements)

        return np.array(fix_list)



    def select(self, indexes):

        """
        Selects Specified Trial By Index Value
        """

        new = copy.deepcopy(self)
        new_data = []
        new_cond = []
        for i in indexes:
            new_data.append(self.data[i])
            new_cond.append(self.conditions[i])
        new.data = new_data
        new.conditions = new_cond

        return new



    def plot_pupil_size(self, trial_num = 1):

        """
        Plots pupil size of a specified trial over a period of time
        """

        index = trial_num - 1
        trial = self.get_trial(trial_num)
        pupil = trial.pupil_size
        plt.plot(range(len(pupil)), pupil)
        plt.title('Pupil_size: Trial %1.f' % trial_num)
        plt.show()



    def plot_tragectory(self, trial_num = 1, image_file = None, screen_size = [1920, 1080]):

        """
        Plots Eye Movement Tragectory for Specified Trial
        """

        index = trial_num - 1
        m = self.get_movement()

        my_dpi = 96
        fig = plt.figure(figsize=(10, 10), dpi=my_dpi)
        # fig.set_size_pixe
        ax = fig.add_subplot(111)

        ax.set_xlim(0,screen_size[0])
        ax.set_ylim(0,screen_size[1])
        ax.plot(m[0][index], m[1][index])
        ax.set_title('Movement: Trial %1.f' % trial_num)
        ax.set_xlabel('Horizontal Eye Movement')
        ax.set_ylabel('Vertical Eye Movement')
        if image_file:
            img = mpimg.imread(image_file)
            # print(img.size)
            new_img = img.resize((screen_size[0], screen_size[1]))
            xsize = int((screen_size[0]-img.shape[0])/2)
            ysize = int((screen_size[1]-img.shape[1])/2)

            imgplot = ax.imshow(img, extent=(xsize, screen_size[0]-xsize, ysize, screen_size[1]-ysize))
            ax.axis('scaled')
            ax.set_xlim(0,screen_size[0])
            ax.set_ylim(0,screen_size[1])
        plt.show()



    def plot_xy(self, trial_num = 1):

        """
        Plots x-coordinates and y-coordinate over a period of time
        """

        index = trial_num - 1
        m = self.get_movement()
        plt.plot(range(len(m[0][index])), m[0][index], label = 'x-axis movement')
        plt.plot(range(len(m[0][index])), m[1][index], label = 'y-axis movement')
        plt.legend()
        plt.title('x-axis vs y-axis Movement: Trial %1.f' % trial_num)
        plt.show()

    def get_x_y(self, data):

        tempX = []
        tempY = []
        x=[]
        y=[]
        for index_1 in data:
            x.append([np.mean(index_1[0]),len(index_1[0])])

        for index_1 in data:
            y.append([np.mean(index_1[1]),len(index_1[1])])

        return np.array(x), np.array(y)

    def get_bubble_plot(self, trial_num = 1, image_file = None, screen_size = [1920, 1080]):

        """
        Will Return A Bubble Plot Of Eye Fixations
        Image Will Be Centered On The Graph

        trial_num:
        find which trial you want to plot

        image_file:
        path to iamge you want to display

        screen_size:
        screen size of computer of screen used during recording
        """

        data = self.get_fixation()
        x,y = self.get_x_y(np.array(data[trial_num-1]))
        xy_list = []

        my_dpi = 96
        fig = plt.figure(figsize=(800/my_dpi, 800/my_dpi), dpi=my_dpi)
        ax = fig.add_subplot(111)

        xi = [xi[0] for xi in x]
        z = np.array([z[1] for z in x])
        yi = [yi[0] for yi in y]

        ax.set_xlim(0,screen_size[0])
        ax.set_ylim(0,screen_size[1])
        ax.scatter(xi, yi, s=z/10, alpha=0.4)

        if image_file:
            img = mpimg.imread(image_file)
            xsize = int((screen_size[0]-img.shape[0])/2)
            ysize = int((screen_size[1]-img.shape[1])/2)
            imgplot = ax.imshow(img, extent=(xsize, screen_size[0]-xsize, ysize, screen_size[1]-ysize))

        plt.show()


class Session(Base):

    """
    Subclass of Base that hold whole trials
        > Reserved for later development for trials
    """

    def __init__(self, trials, sample_rate, conditions=None):
        Base.__init__(self, trials, sample_rate, conditions)



class Epochs(Base):

    """
    Subclass of Base that hold time locking epochs
        > Reserved for later development for Epochs
    """

    def __init__(self, epochs, sample_rate, conditions=None):
        Base.__init__(self, epochs, sample_rate, conditions)
