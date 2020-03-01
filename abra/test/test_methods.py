# method unit testing
from abra import data
from abra import trial
from abra import session
import numpy as np

def test_read_does_not_exist():
    try:
        data.read('abcd*(&3)')
    except OSError as e:
        assert isinstance(e, FileNotFoundError)


def test_read_bad_filename():
    # try:
    #     obj = abra.read('badname.edf')
    # except BadFileExtension:
    #     assert e.errno == errno.ENOENT
    pass


def test_read_file_opened():
    """
    A few test cases for file opening with the Python open function.
    """
    obj = data.read('abra/test/asc/88001.asc')


def test_read_output():
    obj = data.read('abra/test/asc/88001.asc')
    assert isinstance(obj, data.Data)


def test_remove_eye_blinks():
    obj = data.read('abra/test/asc/22205.asc')
    processed = data.pupil_size_remove_eye_blinks(obj, buffer=10)
    assert np.sum(np.isnan(processed.pupil_size))==0
    processed = data.pupil_size_remove_eye_blinks(obj, buffer=100)
    assert np.sum(np.isnan(processed.pupil_size))==0


def test_time_locking():
    obj = data.read('abra/test/asc/22205.asc')
    event_timestamps = [400000, 401000, 402000, 403000, 404000]
    epochs = data.pupil_size_time_locking(obj, event_timestamps = event_timestamps, pre_event=300, post_event=300, baseline=200)
    assert epochs.shape[0] == len(event_timestamps)

def test_split_by_trial():
    obj = data.read('abra/test/asc/22205.asc', mode = 'u')
    sess = obj.split_by_trial()
    assert len(sess.trials) == len(obj.trial_markers['start'])
    assert isinstance(trials[0], data.trial)

def test_summary():
    obj = data.read("abra/test/asc/88001.asc", mode = 'u')
    sess = obj.split_by_trial()
    sum = sess.summary()
    assert isinstance(sum['mean'], float)
    assert isinstance(sum['variance'], float)
    assert isinstance(sum['stdev'], float)
    assert isinstance(sum['length'], float)
    assert isinstance(sum['min'], float)
    assert isinstance(sum['max'], float)
