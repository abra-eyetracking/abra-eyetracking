from scipy import interpolate, signal,stats
from scipy.interpolate import interp1d
from scipy.io import loadmat,savemat
import numpy as np
import re
import copy

#From ABRA
from . import utils
from . import trial
from . import session


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def read(filename, eyes_recorded = "auto", both_eyes_recorded = False, mode="d", start_msg=r"TRIAL \d{1,2} START",
         end_msg=r"TRIAL \d{1,2} END"):
    """
    Read method will read in the ascii file and extract the data
    "file_name" will take in the name of the file you are trying
    to extract data from

    mode: d or u
    d = "defualt"
    u = user defined

    "default" will use the default start and end times given in the file
    "user defined" will take in "start_msg" and "end_msg" to use as the

    eyes_recorded: Define which eye data to extract if both eyes are
                   being recorded
    "left", "right", "auto"
    default is "auto" which will take whichever eye it finds first

    both_eyes_recorded:
    True: if both eyes were recorded
    False: is only the left or right eyes was being recorded

    start and end marker
    "start_msg" will use regular expression to identify the user inputed

    message markers
    ex. r"TRIAL \d START"

    "end_msg" will use regular expression to identify the user inputed end
    message makers
    ex. r"TRIAL \d END"

    Returns Data Object
    """
    # TODO parse info
    if not filename.endswith(".asc"):
        # Raise an error for checking file name extension
        pass
    if not mode == "d" or not mode == "u":
        # raise exception invalid mode
        pass

    with open(filename) as f:
        start_time = ""
        end_time = ""
        flag = False
        events = []
        events_dict = {}
        timestamps_list = []
        messages_dict = {}
        trial_markers = {"start": [], "end": []}
        pupil_size_list = []
        movement_list = [[], []]
        rate_list = {}
        eyes_recorded = eyes_recorded.lower()
        # Default Mode
        if mode == "d":
            for num, line in enumerate(f, 1):
                elements = line.split()

                if line.startswith("START"):
                    start_time, trial_markers, end_time = find_start(elements, start_time, trial_markers, end_time)

                # to only get END messages
                # adds to trial_markers, messages_dict, timestamps_list
                if line.startswith("END"):
                    end_time, trial_markers, messages_dict, flag, start_time = find_end(elements, end_time, trial_markers, messages_dict, flag, start_time)

                if start_time:
                    if line.startswith(start_time):
                        flag = True
                if "RATE" in elements:
                    sample_rate = get_sample_rate(elements, both_eyes_recorded)

                # check for start
                if flag is True:
                    # will get pupil size, timestamps, and movements
                    if is_number(elements[0]):
                        timestamps_list, pupil_size_list, movement_list = tpm_read(timestamps_list, pupil_size_list, movement_list, elements, eyes_recorded, both_eyes_recorded)

                    # Gets all messages between START and END
                    elif elements[0] == "MSG":
                        messages_dict[int(elements[1])] = elements[2:]

                    # Gets all events between START and END
                    elif not is_number(elements[1]):
                        events_dict = event_read(events_dict, elements, eyes_recorded, both_eyes_recorded)


        # User Defined Mode
        elif mode == "u":
            # initializes the regular expressions for start and end markers
            start_msg = re.compile(start_msg)
            end_msg = re.compile(end_msg)
            for num, line in enumerate(f, 1):
                elements = line.split()
                # finds start time using user defined marker
                if re.search(start_msg, line[2:]):
                    start_time, trial_markers, end_time = find_start(elements, start_time, trial_markers, end_time)
                    flag = True
                    continue

                # to only get END messages using user defined marker
                # adds to trial_markers, messages_dict, timestamps_list
                if re.search(end_msg, line[2:]):
                    #print(elements)
                    end_time, trial_markers, messages_dict, flag, start_time = find_end(elements, end_time, trial_markers, messages_dict, flag, start_time)
                    flag = False
                    continue

                if "RATE" in elements:
                    sample_rate = get_sample_rate(elements, both_eyes_recorded)

                # check for start marker
                if flag is True:
                    # will get pupil size, timestamps, and movements
                    if is_number(elements[0]):
                        timestamps_list, pupil_size_list, movement_list = tpm_read(timestamps_list, pupil_size_list, movement_list, elements, eyes_recorded, both_eyes_recorded)
                    # Gets messages between START and END markers
                    elif elements[0] == "MSG":
                        messages_dict[elements[1]] = elements[2:]
                    # Gets all events between START and END markers
                    elif not is_number(elements[1]):
                        events_dict = event_read(events_dict, elements, eyes_recorded, both_eyes_recorded)


    # convert list to numpy array
    timestamps = np.array(timestamps_list)
    pupil_size = np.array(pupil_size_list)
    movement = np.array(movement_list)
    return Data(timestamps, pupil_size, movement, sample_rate, {}, messages_dict,
                events_dict, trial_markers)



def find_start(elements, start_time, trial_markers, end_time):
    """
    Defines Start Times
    - used within read method to find start time of each trial
    - return start timestamp, updates boolean check for start and end
    """
    start_time = elements[1]
    trial_markers["start"].append(int(elements[1]))
    end_time = ""
    return start_time, trial_markers, end_time



def find_end(elements, end_time, trial_markers, messages_dict, flag, start_time):
    """
    Defines End Times
    - used within read method to find start time of each trial
    - return End timestamp, updates boolean check for start and end
    """
    end_time = elements[1]
    trial_markers["end"].append(int(elements[1]))
    messages_dict[int(elements[1])] = elements[2:]
    flag = False
    start_time = ""
    return end_time, trial_markers, messages_dict, flag, start_time


def get_sample_rate(elements, both):
    if both:
        return float(elements[5])
    else:
        return float(elements[4])


def tpm_read(timestamps_list, pupil_size_list, movement_list,
             elements, eyes_recorded, both_eyes_recorded):
    """
    Finds And Returns Timestamps, Pupil Size, and Movements From Each Trial
    """
    if both_eyes_recorded:
        if (eyes_recorded == "left"):
            if(elements[1] == "."):
                timestamps_list.append(int(elements[0]))
                pupil_size_list.append(np.nan)
                movement_list[0].append(np.nan)  # x-axis
                movement_list[1].append(np.nan)
            else:
                timestamps_list.append(int(elements[0]))
                pupil_size_list.append(float(elements[3]))
                movement_list[0].append(float(elements[1]))  # x-axis
                movement_list[1].append(float(elements[2]))  # y-axis

        elif(eyes_recorded == "right"):
            if(elements[4] == "."):
                timestamps_list.append(int(elements[0]))
                pupil_size_list.append(np.nan)
                movement_list[0].append(np.nan)  # x-axis
                movement_list[1].append(np.nan)
            else:
                timestamps_list.append(int(elements[0]))
                pupil_size_list.append(float(elements[6]))
                movement_list[0].append(float(elements[4]))  # x-axis
                movement_list[1].append(float(elements[5]))  # y-axis
        else:
            raise NameError("Define if eyes_recorded was either the left eye or the right eye")
    else:
        if(elements[1] == "."):
            timestamps_list.append(int(elements[0]))
            pupil_size_list.append(np.nan)
            movement_list[0].append(np.nan)  # x-axis
            movement_list[1].append(np.nan)
        else:
            timestamps_list.append(int(elements[0]))
            pupil_size_list.append(float(elements[3]))
            movement_list[0].append(float(elements[1]))  # x-axis
            movement_list[1].append(float(elements[2]))  # y-axis
    return timestamps_list, pupil_size_list, movement_list



def event_read(events_dict, elements, eyes_recorded, both_eyes_recorded):
    """
    Finds And Returns Events
    - Checks if event name already exists before appending
    """
    event_name = f"{elements[0]} {elements[1]}"
    # will extract left or right eye data from recording set set from both eye recordings
    if both_eyes_recorded:
        if(eyes_recorded == "left"):
            if (elements[1] == "R" and event_name not in events_dict):
                events_dict[event_name] = []
        elif(eyes_recorded == "right"):
            if (elements[1] == "R" and event_name not in events_dict):
                events_dict[event_name] = []
        if(event_name in events_dict):
            event_list_variable = elements[2:]
            temp_list = []
            for var in event_list_variable:
                if var == ".":
                    var = np.nan
                    temp_list.append(var)
                else:
                    temp_list.append(float(var))
            event_list_variable = temp_list

            temp_list = list(map(float,temp_list))
            events_dict[event_name].append(temp_list)

    # will extract data from one eye data, 'auto'
    else:
        if event_name not in events_dict:
            events_dict[event_name] = []

        event_list_variable = elements[2:]
        temp_list = []
        for var in event_list_variable:
            if var == ".":
                var = np.nan
                temp_list.append(var)
            else:
                temp_list.append(float(var))
        event_list_variable = temp_list

        temp_list = list(map(float,temp_list))
        events_dict[event_name].append(temp_list)
    return events_dict



def remove_eye_blinks(abra_obj, buffer=50, interpolate='linear', inplace=False):
    """
    The remove_eye_blinks method replaces the eyeblinks (NAS) with
    interpolated data, with a buffer of 50 data points and linear spline
    to do interpolation.
    ### Linear interpolation is what is supported right now.
    """
    ##keep NAs for the movemnt
    #Buffer
    pupilsize_ = np.copy(abra_obj.pupil_size)
    movements_ = np.copy(abra_obj.movement)
    blink_times = np.isnan(pupilsize_)

    for j in range(len(blink_times)):
        if blink_times[j]==True:
            pupilsize_[j-buffer:j+buffer]=np.nan
            movements_[0][j-buffer:j+buffer]=np.nan
            movements_[1][j-buffer:j+buffer]=np.nan
    abra_obj.movement = movements_

    # Interpolate
    interp_move = [[],[]]
    if interpolate=='linear':
        interp_pupil_size = utils.linear_interpolate(pupilsize_)
        # interp_move = utils.linear_interpolate(movements_)
        # interp_move = utils.linear_interpolate(movements_)

        if inplace == True:
            abra_obj.pupil_size = interp_pupil_size
            # abra_obj.pupil_size = interp_move
        elif inplace == False:
            tmp_obj = copy.deepcopy(abra_obj)
            tmp_obj.pupil_size = interp_pupil_size
            # tmp_obj.movement = movements_
            return tmp_obj
    else:
        print("We haven't implement anyother interpolation methods yet")
        return False


def abra_preproc_pupil(data_, dspeed_th = 1, psize_th = 15, smooth=True,sm_window = 101,blink_buffer=50,interp_cluster_th=250,eye_dist_th=15):
    # Remove Blinks
    data = abra.remove_eye_blinks(data_,buffer=blink_buffer,interpolate='linear')

    # Remove sections where eye movements occur
    # Eye movement mask - create a series of distance values from center of screenshot

    # FIRST make spots where distance deviates by more than 3 standard deviations nan.
#     print(data)
    eye_dist = np.sqrt((data.movement[0,:]-np.nanmedian(data.movement[0,:]))**2 + (data.movement[1,:]-np.nanmedian(data.movement[1,:]))**2)
#     eye_dist = np.sqrt((data.movement[0,:]-500)**2 + (data.movement[1,:]-500)**2)

    med_eye_dist = np.nanmedian(eye_dist)
    mad_eye_dist = np.nanmedian(np.absolute(eye_dist - med_eye_dist))

    data.pupil_size[np.greater(eye_dist,med_eye_dist+eye_dist_th*mad_eye_dist,where=~np.isnan(eye_dist))] = np.nan

    # Remove Dilation Speed Outliers
    # This works on the idea that the mean absolute deviation (MAD)
    # gives a good estimate. First, calculate the differenced scores,
    # i.e. the speed of dilation at each time point, then remove
    # timepoints where that dilation speed exceeds the median plus
    # some number of MADs.

    # Note: np.diff returns NAN if either value is NAN, so do this before removing based just on size.

    th_const = dspeed_th

    dspeed_forward = np.absolute(np.diff(data.pupil_size,prepend = np.nanmean(data.pupil_size)))
    dspeed_backward = np.absolute(np.flip(np.diff(np.flip(data.pupil_size),prepend = np.nanmean(data.pupil_size))))
    dspeed = np.fmax(dspeed_forward,dspeed_backward)
    meddspeed = np.nanmedian(dspeed)
    meanad = np.nanmedian(np.absolute(dspeed - meddspeed))

    data.pupil_size[np.greater(dspeed, (meddspeed + th_const*meanad),where=~np.isnan(dspeed))] = np.nan


    # Remove Pupil Size Outliers
    # Easy enough, remove pupil sizes that are greater than three mean absolute
    # deviations from median (avoids being affected by outliers too much).
    # However, this doesn't work as well as using speed.

    # pup_mean = np.nanmean(data.pupil_size)
    # pup_stdev = np.nanstd(data.pupil_size)
    pup_med = np.nanmedian(data.pupil_size)
    pup_mad = np.nanmedian(np.absolute(data.pupil_size - pup_med))

    z_th = 15 # Should be rather large - otherwise you'll end up throwing things out.

    data.pupil_size[np.greater(np.absolute((data.pupil_size - pup_med)/pup_mad),z_th,where=~np.isnan(data.pupil_size))] = np.nan


    # Remove isolated data points

    # TO-DO


    # Interpolate
    # Interpolation to fill missing data.
    mask = ~np.isnan(data.pupil_size)

    # Create a mask where clusters of nans go larger than interp_cluster_th (default 250 points, 500 ms) so we can remove those later.
    # the custom function nan_cluster_mask returns an array the size of data.pupil_size, where it is true everywhere except where
    # there is a continuous stretch of nans longer than interp_cluster_th.
    cluster_mask = nan_cluster_mask(data.pupil_size,interp_cluster_th)
    # Normal interpolation with scipy
    # f = interpolate.interp1d(data.timestamps[mask],
    #                          data.pupil_size[mask],
    #                          kind='linear',
    #                         fill_value=np.nan)
    # data.pupil_size = f(data.timestamps)

    # Interpolation with numpy
    data.pupil_size = np.interp(data.timestamps,
                                data.timestamps[mask],
                                data.pupil_size[mask])

    if smooth:
        data.pupil_size = signal.savgol_filter(data.pupil_size,
                                      window_length = sm_window, # How large of a window for filtering in samples - bigger is more smooth but less fit on original signal
                                      polyorder = 3,
                                      mode = 'nearest')

    # Using the previous nan_cluster_mask (inverted), return the large sections to being nans.
    data.pupil_size[~cluster_mask] = np.nan


    return data

def nan_cluster_mask(signal,threshold):
    # Using the find_nan_clusters function (defined above), we find the starting index and length of every cluster of nans in a signal.
    # Then, we create a mask over signal, similar to isnan, except we return False for spots where the nan clusters are too large.
    # The use-case is for interpolation of data with mostly phasic artifacts where interpolation is fine, but occasionally there would be
    # larger artifacts that we wouldn't want to interpolate over.

    # Note that threshold should be in terms of the sampling frequency of signal.

    nan_idx, nan_lengths = find_nan_clusters(signal)

    # Create the normal mask, where we find all the spots where there are no nans.

    nancluster_mask = np.ones(signal.shape,dtype=bool)


    for i in range(len(nan_lengths)):
        if nan_lengths[i] > threshold:
            nancluster_mask[nan_idx[i]:nan_idx[i]+nan_lengths[i]]=False

    return nancluster_mask

def find_nan_clusters(signal):
    # Find clusters of nans in a list/1D array, return two lists: one with the starting index of each cluster, and the second with
    # the length of the cluster.

    # Four cases:
    # 1. Not in cluster and current value is nan. Need to append nan_idx with index, start counting cluster length.
    # 2. Not in cluster and current value is not nan. No need to do anything.
    # 3. In cluster and current value is nan. Need to keep track of cluster length.
    # 4. In cluster and current value is not nan. Need to end cluster and append nan_lengths with counter - i
    nan_idx = []
    nan_lengths = []
    in_cluster = False

    for i in range(len(signal)):

        if in_cluster:
            if not(np.isnan(signal[i])):
                in_cluster = False
                nan_lengths.append(i-counter)
                counter = 0


        else:
            if np.isnan(signal[i]):
                in_cluster=True
                nan_idx.append(i)
                counter = i

    if len(nan_idx) != len(nan_lengths):
        nan_lengths.append(len(signal)-counter)


    return [nan_idx,nan_lengths]

def sig_smooth(data, sm_window, polyorder = 3, mode = 'nearest'):
    """
    Smooths the signal for pupil size

    Uses scipy.signal savgol_filter

    """
    signal.savgol_filter(data.pupil_size,
                         window_length = sm_window, # How large of a window for filtering in samples - bigger is more smooth but less fit on original signal
                         polyorder = polyorder,
                         mode = mode)


def pre_proc(data, dspeed_th = 0.5, psize_th = 15, sm_window = 151, th_const = 0.5, polyorder = 3, mode = 'nearest'):

    dspeed_forward = np.absolute(np.diff(data[i].pupil_size,prepend = np.nanmean(data[i].pupil_size)))
    dspeed_backward = np.absolute(np.flip(np.diff(np.flip(data[i].pupil_size),prepend = np.nanmean(data[i].pupil_size))))
    dspeed = np.fmax(dspeed_forward,dspeed_backward)
    meddspeed = np.nanmedian(dspeed)
    meanad = np.nanmedian(np.absolute(dspeed - meddspeed))

    data[i].pupil_size[np.greater(dspeed, (meddspeed + th_const*meanad),where=~np.isnan(dspeed))] = np.nan

    pup_med = np.nanmedian(data[i].pupil_size)
    pup_mad = np.nanmedian(np.absolute(data[i].pupil_size - pup_med))

    z_th = psize_th # Should be rather large - otherwise you'll end up throwing things out.

    data[i].pupil_size[np.greater(np.absolute((data[i].pupil_size - pup_med)/pup_mad),z_th,where=~np.isnan(data[i].pupil_size))] = np.nan


    mask = ~np.isnan(data[i].pupil_size)


    # Normal interpolation with scipy
    # f = interpolate.interp1d(data.timestamps[mask],
    #                          data.pupil_size[mask],
    #                          kind='linear',
    #                         fill_value=np.nan)
    # data.pupil_size = f(data.timestamps)

    # Interpolation with numpy
    data[i].pupil_size = np.interp(data[i].timestamps,
                                data[i].timestamps[mask],
                                data[i].pupil_size[mask])



    pup_data = signal.savgol_filter(data[i].pupil_size,
                                      window_length = sm_window, # How large of a window for filtering in samples - bigger is more smooth but less fit on original signal
                                      polyorder = 3,
                                      mode = 'nearest')

    data[i].pupil_size = pup_data

    return data



class Data:
    """
    The Data class for the data structure

    Use read function to create Data object

    - Stores data values of timestamps, pupil_size, movement, sample_rate,
      calibration, messages, events, trial_markers
    - Value Types:
        - timestamps: List (1xn)
        - pupil_size: List (1xn)
        - Movement: List (2xn)
            > index 0: x-coordinates
            > index 1: y-coordinates
        - sample_rate: int
        -calibration: Dictionary (not implimented yet)
        - message: Dictionary
            > key: timestamp integer
            > value: message
        - events: Dictionary
            > key: event name
            > value: list of [start timestamp, end timestamp,
                              avg y-coordinate, avg x-coordinate,
                              avg pupil size]
        - trial_markers: Dictionary
            > key: 'Start' or 'End'
            > value: list of time stamps
    """
    def __init__(self, timestamps, pupil_size, movement, sample_rate,
                 calibration, messages, events, trial_markers):
        self.timestamps = timestamps
        self.pupil_size = pupil_size
        self.movement = movement
        self.sample_rate = sample_rate
        self.calibration = calibration
        self.messages = messages
        self.events = events
        self.trial_markers = trial_markers



    def create_session(self, conditions=None):
        """
        This function splits the pupil size and timestamp data into
        its respective trials and returns an array of trial class
        objects

        condition: event condition
        """
        t_Mark = self.trial_markers
        t_Time = self.timestamps
        start = t_Mark['start']
        end  = t_Mark['end']

        # All trial start and end markers in array ([start,end])
        trial_IDX = []
        for i in range(len(start)):
            temp = []
            st = start[i]
            en = end[i]
            temp.append(st)
            temp.append(en)
            trial_IDX.append(temp)

        # Get the pupil size in the events between the starting and ending markers
        trial_pupil = []
        trial_mov_x = []
        trial_mov_y = []
        trial_stamp = []
        trial_event_L_fix = []
        trial_event_R_fix = []
        index_L = 0
        index_R = 0
        for i in range(len(trial_IDX)):
            st = trial_IDX[i][0]
            en = trial_IDX[i][1]

            # Find the indexes to call the pupil size within the timestamps for a trial
            idx = np.where((self.timestamps >= st) & (self.timestamps <= en))[0]

            # Add the pupil sizes for each timestamp
            temp_pupil = []
            temp_movex = []
            temp_movey = []
            temp_stamp = []
            temp_L_event = []
            temp_R_event = []
            for k in idx:
                temp_pupil.append(self.pupil_size[k])
                temp_stamp.append(self.timestamps[k])
                temp_movex.append(self.movement[0][k])
                temp_movey.append(self.movement[1][k])
                if('EFIX L' in self.events and index_L < len(self.events['EFIX L']) and self.events['EFIX L'][index_L][1] == self.timestamps[k]):
                    temp_L_event.append(self.events['EFIX L'][index_L])
                    index_L += 1
                if('EFIX R' in self.events and index_R < len(self.events['EFIX R']) and self.events['EFIX R'][index_R][1] == self.timestamps[k]):
                    temp_R_event.append(self.events['EFIX R'][index_R])
                    index_R += 1
            trial_pupil.append(np.array(temp_pupil))
            trial_mov_x.append(np.array(temp_movex))
            trial_mov_y.append(np.array(temp_movey))
            trial_stamp.append(np.array(temp_stamp))
            trial_event_L_fix.append(np.array(temp_L_event))
            trial_event_R_fix.append(np.array(temp_R_event))


        # Create a list of new trials with each pupil_size
        trials = []
        for i in range(len(trial_IDX)):
            t = trial.Trial(trial_stamp[i], trial_pupil[i],
                            trial_mov_x[i], trial_mov_y[i],
                            trial_event_L_fix[i], trial_event_R_fix[i])
            trials.append(t)

        # Check for conditions
        num_trials = len(trials)
        if conditions is not None:
            if (len(conditions) != num_trials):
                raise ValueError('Condition length must be equal to the number of trials: ', num_trials)

        return session.Session(np.array(trials), self.sample_rate, conditions)

    def create_epochs(self, event_timestamps, conditions=None, pre_event=200, post_event=200, pupil_baseline=None):
        """
        Create Time Locking Epochs

        event_timestamps: starting timestamps for all time locking events
        conditions: event condition
        pre_event: milliseconds before defined starting timestamps
        post_event: milliseconds after defined starting timestamps
        pupil_baseline: Baselining for pupil size data,
                        baseline period will be the milliseconds
                        before pre_event
        """

        #Create an empty array for storing the epoch information
        win_size = int((pre_event+post_event)*self.sample_rate/1000)
        all_epochs = []

        # Iterate timestamp events get each epoch pupil size
        for i in range(len(event_timestamps)):
            start = event_timestamps[i]-pre_event
            end = event_timestamps[i]+post_event
            idx = (self.timestamps >= (event_timestamps[i]-pre_event)) & (self.timestamps <= (event_timestamps[i]+post_event))

            if np.sum(idx) != win_size:
                non_zero_idx = np.nonzero(idx)

                # Explicitly set all values beyond window size to False
                # Enforcing the length to be the defined window size
                idx[non_zero_idx[0][0]+win_size:]=False
            epoch_pupil = self.pupil_size[idx]
            epoch_movex = self.movement[0][idx]
            epoch_movey = self.movement[1][idx]

            # Do baselining using the mean and standard deviation of the mean and variance
            if pupil_baseline:
                baseline_idx = (self.timestamps >= (event_timestamps[i]-pre_event+pupil_baseline[0])) & (self.timestamps <= (event_timestamps[i]-pre_event+pupil_baseline[1]))
                baseline_period = self.pupil_size[baseline_idx]
                baseline_mean = np.mean(baseline_period)
                baseline_std = np.std(baseline_period)
                epoch_pupil = (epoch_pupil - baseline_mean)/baseline_std

            t = trial.Trial(self.timestamps[idx], epoch_pupil, epoch_movex, epoch_movey)
            all_epochs.append(t)

        epochs = session.Epochs(all_epochs, self.sample_rate, conditions)
        return epochs
