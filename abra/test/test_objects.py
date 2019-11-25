# object unit testing
from abra import data
import numpy as np
from time import sleep


def test_data_object():
    data_test = data.Data()
    assert data_test.pupil_size.size == 0
    assert data_test.movement.size == 0
    assert data_test.timestamps.size == 0
    assert data_test.sample_rate == 0
    assert not data_test.messages
    assert not data_test.events
    assert not data_test.calibration

def test_data_object_array_dimensions():
    data_test = data.Data()
    assert data_test.pupil_size.ndim == 1
    assert data_test.movement.ndim == 2
    assert data_test.timestamps == 1

def test_data_object_data_type():
    data_test = data.Data()
    assert type(data_test.pupil_size) == np.ndarray 
    assert type(data_test.movement) == np.ndarray 
    assert type(data_test.timestamps) == np.ndarray
    assert type(data_test.sample_rate) == int
    assert type(data_test.messages) == dict
    assert type(data_test.events) == dict
    assert type(data_test.calibration) == dict

