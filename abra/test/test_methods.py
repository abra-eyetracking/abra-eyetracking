# method unit testing
from abra import data


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
            
def test_remove_eye_blink():
    obj = data.read('abra/test/asc/88001.asc')
    obj = data.remove_eye_blink(obj)
    if mode=='remove':
        movement_x_has_nan = (np.nan in obj.movement[:,0])
        movement_y_has_nan = (np.nan in obj.movement[:,1])
        pupil_size_has_nan = (np.nan in obj.pupil_size)
        assert movement_x_has_nan == True
        assert movement_y_has_nan == True
        assert pupil_size_has_nan == True

    movement_x_has_no_zero = (0 not in obj.movement[:,0])
    movement_y_has_no_zero = (0 not in obj.movement[:,1])
    pupil_size_has_no_zero = (0 not in obj.pupil_size)
    assert movement_x_has_no_zero == True
    assert movement_y_has_no_zero == True
    assert pupil_size_has_no_zero == True
    assert isinstance(obj, data.Data)
