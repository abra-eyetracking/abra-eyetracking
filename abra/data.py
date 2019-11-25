import numpy as np


def read(filename):
    # TODO parse info
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
