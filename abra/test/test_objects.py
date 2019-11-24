# object unit testing
import abra
from time import sleep


def test_data_object1():
    data_test = Data()
    assert data_test.pupil_size == [], "should be empty (1 * n_t) "  # (1 * n_t)
    assert data_test.movement == [][], "should be empty (1 * n_t) "  # (2 * n_t)
    assert data_test.timestamps == [], "should be empty (1 * n_t) "  # (1 * n_t)
    assert data_test.sample_rate == 0, "should be empty int"         # (int)
    assert data_test.messages == {}, " should be empty dict"         # (dict)
    assert data_test.events == {}, " should be empty dict"           # (dict)
    assert data_test.calibration == {}, "should be empty dict"       # (dict)
    assert True


def test_object2():
    sleep(.1)
    assert True

