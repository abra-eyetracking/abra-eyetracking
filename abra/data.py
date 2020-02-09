import numpy as np
import re


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


"""
Read method will read in the ascii file and extract the data
"file_name" will take in the name of the file you are trying
to extract data from
mode: d or u
d = "defualt"
u = user defined
"default" will use the default start and end times given in the file
"user defined" will take in "start_msg" and "end_msg" to use as the
start and end marker
"start_msg" will use regular expression to identify the user inputed
message markers
ex. r"TRIAL \d START"
"end_msg" will use regular expression to identify the user inputed end
message makers
ex. r"TRIAL \d END"
"""


def read(filename, mode="d", start_msg=r"TRIAL \d{1,2} START",
         end_msg=r"TRIAL \d{1,2} END", autoepoch=False):
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

        # Default Mode
        if mode == "d":
            for num, line in enumerate(f, 1):
                elements = line.split()

                if line.startswith("START"):
                    start_time = elements[1]
                    trial_markers["start"].append(elements[1])
                    end_time = ""  # to end "END message input"

                # to only get END messages
                # adds to trial_markers, messages_dict, timestamps_list
                if line.startswith("END"):
                    end_time = elements[1]
                    trial_markers["end"].append(elements[1])
                    messages_dict[elements[1]] = elements[2:]
                    flag = False
                    start_time = ""

                if start_time:
                    if line.startswith(start_time):
                        flag = True

                if "RATE" in line.upper():
                    elements = line.upper().split()
                    rate_index = elements.index("RATE")
                    rate_list[start_time] = elements[rate_index+1]

                # check for start
                if flag is True:
                    # will get pupil size, timestamps, and movements
                    if is_number(elements[0]):
                        timestamps_list.append(elements[0])
                        pupil_size_list.append(elements[1])
                        movement_list[0].append(elements[2])  # x-axis
                        movement_list[1].append(elements[3])  # y-axis
                    # Gets all messages between START and END
                    elif elements[0] == "MSG":
                        messages_dict[elements[1]] = elements[2:]
                    # Gets all events between START and END
                    elif not is_number(elements[1]):
                        events.append(elements[0])
                        # check if event already exist
                        event_name = f"{elements[0]} {elements[1]}"
                        if event_name not in events_dict:
                            events_dict[event_name] = elements[2:]
                        else:
                            events_dict[event_name].append(elements[2:])

                # finds all the END messages that is outputed
                if end_time:
                    if line.startswith("MSG"):
                        if elements[1] in messages_dict:
                            messages_dict[elements[1]].append(elements[2:])
                        else:
                            messages_dict[elements[1]] = elements[2:]
        # User Defined Mode
        elif mode == "u":
            # initializes the regular expressions for start and end markers
            start_msg = re.compile(start_msg)
            end_msg = re.compile(end_msg)
            for num, line in enumerate(f, 1):
                elements = line.split()
                # finds start time using user defined marker
                if re.search(start_msg, line[2:]):
                    start_time = elements[1]
                    trial_markers["START"].append(elements[1])
                    end_time = ""  # to end "END message input"

                # to only get END messages using user defined marker
                # adds to trial_markers, messages_dict, timestamps_list
                if re.search(end_msg, line[2:]):
                    end_time = elements[1]
                    trial_markers["END"].append(elements[1])
                    messages_dict[elements[1]] = elements[2:]
                    flag = False
                    start_time = ""

                if start_time:
                    if line.startswith(start_time):
                        flag = True
                if "RATE" in line.upper():
                    elements = line.upper().split()
                    rate_index = elements.index("RATE")
                    rate_list[start_time] = elements[rate_index+1]
                # check for start marker
                if flag is True:
                    # will get pupil size, timestamps, and movements
                    if is_number(elements[0]):
                        timestamps_list.append(elements[0])
                        pupil_size_list.append(elements[1])
                        movement_list[0].append(elements[2])  # x-axis
                        movement_list[1].append(elements[3])  # y-axis
                    # Gets messages between START and END markers
                    elif elements[0] == "MSG":
                        messages_dict[elements[1]] = elements[2:]
                    # Gets all events between START and END markers
                    elif not is_number(elements[1]):
                        events.append(elements[0])
                        # checks if event already exists
                        event_name = f"{elements[0]} {elements[1]}"
                        if event_name not in events_dict:
                            events_dict[event_name] = elements[2:]
                        else:
                            events_dict[event_name].append(elements[2:])

                # finds all the END messages that is outputed
                if end_time:
                    if line.startswith("MSG"):
                        if elements[1] in messages_dict:
                            messages_dict[elements[1]].append(elements[2:])
                        else:
                            messages_dict[elements[1]] = elements[2:]


# remove duplicates
    timestamps_list = list(dict.fromkeys(timestamps_list))
    # convert list to numpy array
    timestamps = np.array(timestamps_list)
    pupil_size = np.array(pupil_size_list)
    movement = np.array(movement_list)
    return Data(timestamps, pupil_size, movement, 500, {}, messages_dict,
                events_dict, trial_markers)


class Data:

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

    def trial_start():
        pass

    def trial_end():
        pass
