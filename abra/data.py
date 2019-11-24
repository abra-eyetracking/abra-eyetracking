import numpy as np
from time import sleep


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def read(filename):
    # TODO parse info
    if not filename.endswith('.asc'):
        # Raise an error for checking file name extension
        pass


    with open(filename) as f:
        start_time = ''
        flag = False
        events = []
        for num, line in enumerate(f, 1):
            elements = line.split()
            if line.startswith('START'):
                # Find the starting time asshole
                start_time = elements[1]

            if start_time:
                if line.startswith(start_time):
                    flag = True

            if flag == True:
                if not is_number(elements[0]):
                    events.append(elements[0])


        print(np.unique(events))
        input()





    return Data()

class Data:

    def __init__(self):
        # TODO implement initialization
        #   pupil_size (1 * n_t)
        #   movement (2 * n_t)
        #   timestamps (1 * n_t)
        #   sample_rate (int)
        #   messages (dict)
        #   events (dict)
        #   calibration (dict)
        pass

    def trial_start():
        pass

    def trial_end():
        pass
