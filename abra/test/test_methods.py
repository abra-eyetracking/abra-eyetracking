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
