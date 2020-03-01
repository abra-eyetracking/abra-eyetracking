# object unit testing
from abra import data
import numpy as np


def test_data_object_init():
    obj = data.read("abra/test/asc/88001.asc")
    type(obj)
    # TODO: test initialized object members instead of empty
    #   bottom code is for empty Data() obj which we will not allow,
    #   i.e. Data() init MUST be passed parameters (from read),
    #   users will NOT be allowed to create Data() obj manually.

    #   Will not use:
    # assert obj.timestamps.size == 0
    # assert obj.pupil_size.size == 0
    # assert obj.movement.size == 0
    # assert obj.sample_rate == 0
    # assert not obj.calibration
    # assert not obj.messages
    # assert not obj.events


def test_data_member_dimensions():
    obj = data.read("abra/test/asc/88001.asc")
    assert obj.timestamps.ndim == 1
    assert obj.pupil_size.ndim == 1
    assert obj.movement.ndim == 2


def test_data_member_types():
    obj = data.read("abra/test/asc/88001.asc")
    assert isinstance(obj.timestamps, np.ndarray)
    assert isinstance(obj.pupil_size, np.ndarray)
    assert isinstance(obj.movement, np.ndarray)
    assert isinstance(obj.sample_rate, int)
    assert isinstance(obj.calibration, dict)
    assert isinstance(obj.messages, dict)
    assert isinstance(obj.events, dict)


def test_data_missing_values_user():
    obj = data.read(filename = "abra/test/asc/22205.asc", mode = "u",
                    start_msg = r"b'TRIAL \d{1,2} STARTS",
                    end_msg = r"b'TRIAL \d{1,2} ENDS'")
    assert None not in obj.timestamps
    # for x in obj.timestamps:
        # assert x is not None
#     for x in obj.pupil_size:
#         assert x is not None
#     for x in obj.movement[0]:
#         assert x is not None
#     for x in obj.movement[1]:
#         assert x is not None
#     for x in obj.messages:
#         assert obj.messages[x] is not None
#     for x in obj.events:
#         assert obj.events[x] is not None
#     for x in obj.trial_markers["start"]:
#         assert x is not None
#     for x in obj.trial_markers["end"]:
#         assert x is not None
# def test_data_missing_values_default():
#     obj = data.read(filename = "88001.asc"
#     for x in obj.timestamps:
#         assert x is not None
#     for x in obj.pupil_size:
#         assert x is not None
#     for x in obj.movement[0]:
#         assert x is not None
#     for x in obj.movement[1]:
#         assert x is not None
#     for x in obj.messages:
#         assert obj.messages[x] is not None
#     for x in obj.events:
#         assert obj.events[x] is not None
#     for x in obj.trial_markers["start"]:
#         assert x is not None
#     for x in obj.trial_markers["end"]:
#         assert x is not None
