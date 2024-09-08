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

    # In this conext, n=1 would be recursive, so always
    # return 2.
    assert common.get_next_fibonacci(0) == 1
    assert common.get_next_fibonacci(1) == 2
    assert common.get_next_fibonacci(2) == 3
    assert common.get_next_fibonacci(4) == 5
    assert common.get_next_fibonacci(10) == 13
    assert common.get_next_fibonacci(15) == 21
    assert common.get_next_fibonacci(30) == 34

def test_get_prev_fibonacci():
    assert common.get_prev_fibonacci(33) == 21
    assert common.get_prev_fibonacci(34) == 21
    assert common.get_prev_fibonacci(21) == 13
    assert common.get_prev_fibonacci(13) == 8
    assert common.get_prev_fibonacci(8) == 5
    assert common.get_prev_fibonacci(5) == 3
    assert common.get_prev_fibonacci(3) == 2
    assert common.get_prev_fibonacci(2) == 1

    # Recursive, always assume 0 for previous
    assert common.get_prev_fibonacci(1) == 0

def test_get_fibonacci():
    fibs = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    for index, value in enumerate(fibs):
        assert common.get_fibonacci(index) == value

    with pytest.raises(ValueError):
        common.get_fibonacci(-1)
