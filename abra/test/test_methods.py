# method unit testing
import abra
from time import sleep


def test_read_does_not_exist():
    try:
        obj = abra.read('abcd*(&3)')
    except OSError as e:
        assert e.errno == errno.ENOENT


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
    obj = abra.read('asc/88001.asc')

def test_read_output():
    obj = abra.read('asc/88001.asc')
    assert type(obj) == type(abra.Data())

