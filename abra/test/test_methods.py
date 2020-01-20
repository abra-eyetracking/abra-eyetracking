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
    obj = data.read('test/asc/88001.asc')


def test_read_output():
    obj = data.read('test/asc/88001.asc')
    assert isinstance(obj, data.Data)
