# method unit testing
from abra import data
from abra import trial
from abra import session
import numpy as np

default_obj = data.read('abra/test/asc/1211NE1.asc')
udef_obj = data.read('abra/test/asc/22205.asc', mode = 'u')

def test_read_output():
    assert isinstance(default_obj, data.Data)
    assert isinstance(udef_obj, data.Data)


def test_remove_eye_blinks():
    processed = data.pupil_size_remove_eye_blinks(default_obj, buffer=10)
    assert np.sum(np.isnan(processed.pupil_size))==0
    processed = data.pupil_size_remove_eye_blinks(default_obj, buffer=100)
    assert np.sum(np.isnan(processed.pupil_size))==0

    processed = data.pupil_size_remove_eye_blinks(udef_obj, buffer=10)
    assert np.sum(np.isnan(processed.pupil_size))==0
    processed = data.pupil_size_remove_eye_blinks(udef_obj, buffer=100)
    assert np.sum(np.isnan(processed.pupil_size))==0

def test_shuffle():
    sess = default_obj.create_session()
    sess_u = udef_obj.create_session()
    cleaned_default = data.pupil_size_remove_eye_blinks(default_obj, buffer=50)
    event_timestamps = np.array(cleaned_default.trial_markers['start']) + 1000  # Buffer for baslining
    test_epochs = cleaned_default.create_epochs(event_timestamps,
                                                conditions=None,
                                                pre_event=200,
                                                post_event=200,
                                                pupil_baseline=[-200,-100])
    rand_shuf = session.shuffle(test_epochs)

    assert isinstance(rand_shuf, session.Epochs)
    for i in rand_shuf.data:
        assert i in test_epochs.data

    cleaned_udef = data.pupil_size_remove_eye_blinks(udef_obj, buffer=50)
    event_timestamps = np.array(cleaned_udef.trial_markers['start']) + 1000  # Buffer for baslining
    test_epochs_udef = cleaned_udef.create_epochs(event_timestamps,
                                                conditions=None,
                                                pre_event=200,
                                                post_event=200,
                                                pupil_baseline=[-200,-100])
    rand_shuf = session.shuffle(test_epochs_udef)
    assert isinstance(rand_shuf, session.Epochs)
    for i in rand_shuf.data:
        assert i in test_epochs_udef.data

    rand_sess = session.shuffle(sess)
    assert isinstance(rand_sess, session.Session)
    for i in rand_sess.data:
        assert i in sess.data


    rand_sess= session.shuffle(sess_u)
    assert isinstance(rand_sess, session.Session)
    for i in rand_sess.data:
        assert i in sess_u.data
