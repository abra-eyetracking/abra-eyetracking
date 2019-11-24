# object unit testing

import abra
import numpy as np
from time import sleep


def test_data_object():
    data_test = Data()
    assert data_test.pupil_size == [], "should be empty (1 * n_t) "  # (1 * n_t)
    assert data_test.movement == [][], "should be empty (2 * n_t) "  # (2 * n_t)
    assert data_test.timestamps == [], "should be empty (1 * n_t) "  # (1 * n_t)
    assert data_test.sample_rate == 0, "should be empty int"         # (int)
    assert data_test.messages == {}, " should be empty dict"         # (dict)
    assert data_test.events == {}, " should be empty dict"           # (dict)
    assert data_test.calibration == {}, "should be empty dict"       # (dict)

def test_data_object_array_dimensions():
    data_test = Data()
    assert data_test.pupil_size.ndim == 1
    assert data_test.movement.ndim == 2
    assert data_test.timestamps == 1

def test_data_object_data_type():
    data_test = Data()
    assert type(data_test.pupil_size) == np.ndarray 
    assert type(data_test.movement) == np.ndarray 
    assert type(data_test.timestamps) == np.ndarray
    assert type(data_test.sample_rate) == int
    assert type(data_test.messages) == dict
    assert type(data_test.events) == dict
    assert type(data_test.calibration) == dict


def test_object2():
    sleep(.1)
    assert True

