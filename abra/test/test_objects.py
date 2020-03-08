# object unit testing
from abra import data
from abra import trial
from abra import session
import numpy as np


default_obj = data.read("abra/test/asc/1211NE1.asc")
udef_obj = data.read("abra/test/asc/22205.asc", mode = 'u')

def test_data_member_dimensions():
    assert default_obj.timestamps.ndim == 1
    assert default_obj.pupil_size.ndim == 1
    assert default_obj.movement.ndim == 2

    assert udef_obj.timestamps.ndim == 1
    assert udef_obj.pupil_size.ndim == 1
    assert udef_obj.movement.ndim == 2


def test_data_member_types():
    assert isinstance(default_obj.timestamps, np.ndarray)
    assert isinstance(default_obj.pupil_size, np.ndarray)
    assert isinstance(default_obj.movement, np.ndarray)
    assert isinstance(default_obj.sample_rate, int)
    assert isinstance(default_obj.calibration, dict)
    assert isinstance(default_obj.messages, dict)
    assert isinstance(default_obj.events, dict)

    assert isinstance(udef_obj.timestamps, np.ndarray)
    assert isinstance(udef_obj.pupil_size, np.ndarray)
    assert isinstance(udef_obj.movement, np.ndarray)
    assert isinstance(udef_obj.sample_rate, int)
    assert isinstance(udef_obj.calibration, dict)
    assert isinstance(udef_obj.messages, dict)
    assert isinstance(udef_obj.events, dict)

def test_trial_object():
    # Test for default case:
    sess = default_obj.create_session()
    for t in sess.data:
        assert isinstance(t, trial.Trial)
        assert t.timestamps.ndim == 1
        assert t.pupil_size.ndim == 1
        assert isinstance(t.timestamps, np.ndarray)
        assert isinstance(t.pupil_size, np.ndarray)

        sum = t.summary()
        assert isinstance(sum['mean'], float)
        assert isinstance(sum['variance'], float)
        assert isinstance(sum['stdev'], float)
        assert isinstance(sum['length'], int)
        assert isinstance(sum['min'], float)
        assert isinstance(sum['max'], float)

    # Test for user define case:
    sess = udef_obj.create_session()
    for t in sess.data:
        assert isinstance(t, trial.Trial)
        assert t.timestamps.ndim == 1
        assert t.pupil_size.ndim == 1
        assert isinstance(t.timestamps, np.ndarray)
        assert isinstance(t.pupil_size, np.ndarray)

        sum = t.summary()
        assert isinstance(sum['mean'], float)
        assert isinstance(sum['variance'], float)
        assert isinstance(sum['stdev'], float)
        assert isinstance(sum['length'], int)
        assert isinstance(sum['min'], float)
        assert isinstance(sum['max'], float)

def test_session_object():
    sess = default_obj.create_session()
    assert isinstance(sess, session.Session)
    #assert isinstance(sess.data, list)
    assert isinstance(sess.data[0], trial.Trial)
    assert isinstance(sess.conditions, np.ndarray)
    assert len(sess.data) == len(sess.conditions)

    sum = sess.summary()
    assert isinstance(sum['mean'], float)
    assert isinstance(sum['variance'], float)
    assert isinstance(sum['stdev'], float)
    assert isinstance(sum['length'], int)
    assert isinstance(sum['min'], float)
    assert isinstance(sum['max'], float)

    index = [0,1,5,7,8,4,20,15,14,22,30]
    selected = sess.select(index)
    assert isinstance(selected, session.Session)
    assert len(selected.data) == len(index)
    
    sess = udef_obj.create_session()
    assert isinstance(sess, session.Session)
    #assert isinstance(sess.data, list)
    assert isinstance(sess.data[0], trial.Trial)
    assert isinstance(sess.conditions, np.ndarray)
    assert len(sess.data) == len(sess.conditions)

    sum = sess.summary()
    assert isinstance(sum['mean'], float)
    assert isinstance(sum['variance'], float)
    assert isinstance(sum['stdev'], float)
    assert isinstance(sum['length'], int)
    assert isinstance(sum['min'], float)
    assert isinstance(sum['max'], float)

    index = [0,1,5,7,8,4,20,15,14,22,30]
    selected = sess.select(index)
    assert isinstance(selected, session.Session)
    assert len(selected.data) == len(index)

def test_epochs_object():
    cleaned_default = data.pupil_size_remove_eye_blinks(default_obj, buffer=50)
    event_timestamps = np.array(cleaned_default.trial_markers['start']) + 1000  # Buffer for baslining
    test_epochs = cleaned_default.create_epochs(event_timestamps,
                                                conditions=None,
                                                pre_event=200,
                                                post_event=200,
                                                pupil_baseline=[-200,-100])
    sum = test_epochs.summary()
    assert isinstance(sum['mean'], float)
    assert isinstance(sum['variance'], float)
    assert isinstance(sum['stdev'], float)
    assert isinstance(sum['length'], int)
    assert isinstance(sum['min'], float)
    assert isinstance(sum['max'], float)

    assert test_epochs.get_values().shape[1] == 200

    index = [0,1,5,7,8,4,20,15,14,22,30]
    selected = test_epochs.select(index)

    assert isinstance(selected, session.Epochs)
    assert len(selected.data) == len(index)

    cleaned_udef = data.pupil_size_remove_eye_blinks(udef_obj, buffer=50)
    event_timestamps = np.array(cleaned_udef.trial_markers['start']) + 1000  # Buffer for baslining
    test_epochs = cleaned_udef.create_epochs(event_timestamps,
                                                conditions=None,
                                                pre_event=200,
                                                post_event=200,
                                                pupil_baseline=[-200,-100])
    sum = test_epochs.summary()
    assert isinstance(sum['mean'], float)
    assert isinstance(sum['variance'], float)
    assert isinstance(sum['stdev'], float)
    assert isinstance(sum['length'], int)
    assert isinstance(sum['min'], float)
    assert isinstance(sum['max'], float)

    assert test_epochs.get_values().shape[1] == 200

    index = [0,1,5,7,8,4,20,15,14,22,30]
    selected = test_epochs.select(index)

    assert isinstance(selected, session.Epochs)
    assert len(selected.data) == len(index)
