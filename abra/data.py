import numpy as np
from time import sleep


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def read(filename, mode = "default"):
    # TODO parse info
    if not filename.endswith('.asc'):
        # Raise an error for checking file name extension
        pass


    with open(filename) as f:
        start_time = ''
        end_time = ''
        flag = False
        events = []
        events_dict = {}
        timestamps_list = []
        messages_dict = {}
        trial_markers = {"start":[], "end":[]}
        if mode == "default":
            for num, line in enumerate(f, 1):
                elements = line.split()
                if line.startswith('START'):
                    # Find the starting time asshole
                    start_time = elements[1]
                    trial_markers["start"].append(elements[1])
                    end_time = ''   #to end "END message input"
                    timestamps_list.append(elements[1])
                #to only get END messages
                if line.startswith('END'):
                    end_time = elements[1]
                    trial_markers["end"].append(elements[1])
                    messages_dict[elements[1]] = elements[2:]
                    timestamps_list.append(elements[1])
                    flag = False
                    start_time = ''

                if start_time:
                    if line.startswith(start_time):
                        flag = True
                # check for start
                if flag == True:
                    #gets messages between default start and end
                    if elements[0] == "MSG":
                        timestamps_list.append(elements[1])
                        messages_dict[elements[1]] = elements[2:]
                    elif not is_number(elements[1]):
                        events.append(elements[0])
                        if str(elements[0] + " " + elements[1]) not in events_dict:
                            events_dict[str(elements[0] + " " + elements[1])] = elements[2:]
                            timestamps_list.append(elements[2])
                        else:
                            events_dict[str(elements[0] + " " + elements[1])].append(elements[2:])
                            timestamps_list.append(elements[2])

                    else:
                        timestamps_list.append(elements[0])

                #finds all the END messages that is outputed
                if end_time:
                    if line.startswith('MSG'):
                        if elements[1] in messages_dict:
                            messages_dict[elements[1]].append(elements[2:])
                        else:
                            messages_dict[elements[1]] = elements[2:]
        print(np.unique(events))
        input()





    return Data()


class Data:

    def __init__(self, timestamps, pupil_size, movement, sample_rate,
                 calibration, messages, events):
        self.timestamps = timestamps
        self.pupil_size = pupil_size
        self.movement = movement
        self.sample_rate = sample_rate
        self.calibration = calibration
        self.messages = messages
        self.events = events

    def trial_start():
        pass

    def trial_end():
        pass
