import pytest
from seed import common

def test_is_fibonacci():
    fibs = [1, 2, 3, 5, 8, 13, 21, 34]
    non_fibs = [-1,4,6,7,9,10,20,30,54,100]

    for n in fibs:
        assert common.is_fibonacci(n)

    for n in non_fibs:
        assert not common.is_fibonacci(n)

def test_get_next_fibonacci():
    assert common.get_next_fibonacci(1) == 1
    assert common.get_next_fibonacci(2) == 3
    assert common.get_next_fibonacci(4) == 5
    assert common.get_next_fibonacci(10) == 13
    assert common.get_next_fibonacci(15) == 21
    assert common.get_next_fibonacci(30) == 34

def test_get_fibonacci():
    fibs = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    for index, value in enumerate(fibs):
        assert common.get_fibonacci(index) == value

    with pytest.raises(ValueError):
        common.get_fibonacci(-1)
