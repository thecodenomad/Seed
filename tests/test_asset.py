import json
import pytest

from pydantic_core import from_json
from seed.models import Asset
from seed import common, errors

pytestmark = pytest.mark.asset

@pytest.fixture(scope="function")
def basic_asset_dict(basic_asset_json):
    obj = json.loads(basic_asset_json)
    yield obj

@pytest.fixture(scope="function")
def basic_asset_hashtags(basic_asset_dict):
    yield basic_asset_dict["descriptors"]

@pytest.fixture(scope="function")
def basic_asset(basic_asset_json):
    yield Asset.model_validate_json(basic_asset_json)

def test_add_and_remove_descriptor(basic_asset):

    descriptors = ["hecklefish", "hecklefish1", "hecklefish2", "hecklefish3"]
    for i in descriptors:
        basic_asset.add_descriptor(i)
        assert basic_asset.next_fib == common.get_next_fibonacci(len(basic_asset.descriptors))

    # It should currently be uneven
    assert basic_asset.is_uneven()

    for i in descriptors:
        basic_asset.remove_descriptor(i)
        assert basic_asset.next_fib == common.get_next_fibonacci(len(basic_asset.descriptors))

    # It should currently be even
    assert not basic_asset.is_uneven()

def test_basic_asset(basic_asset, basic_asset_dict):
    """ Validate the values from the basic json file. """

    # Attribute Validations
    assert basic_asset.name == basic_asset_dict["name"]
    assert basic_asset.next_fib == basic_asset_dict["next_fib"]
    assert basic_asset.level_up == True
    assert basic_asset.descriptors == {"1","1.0"}

def test_basic_asset_hashtags(basic_asset, basic_asset_hashtags):
    valid_hastags = ["desc1", "desc2"]
    # Validate the hashtags used in the json file
    for i in basic_asset.hashtags:
        assert i in basic_asset_hashtags

def test_level_up_asset(basic_asset):
    # At the start of this test, the basic asset has 2 descriptors
    assert basic_asset.next_fib == 3

    descriptors = ["hecklefish", "hecklefish1", "hecklefish2", "hecklefish3"]
    next_fib = [5,5,8,8]

    for index,i in enumerate(descriptors):
        basic_asset.add_descriptor(i)
        assert basic_asset.next_fib == next_fib[index]
        assert basic_asset.level_up == common.is_fibonacci(len(basic_asset.descriptors))


def test_invalid_basic_asset():
    """ Validate the values from the basic json file. """

    # Level up should fail because the number of descriptors is indeed a Fibonacci number
    model_to_validate = {
        "name": "character",
        "descriptors": ["1", "1.0"],
        "next_fib": 3,
        "level_up": False,
        "strict": True
    }

    model_json = json.dumps(model_to_validate)
    with pytest.raises(errors.SeedValidationException):
        model_to_validate = Asset.model_validate_json(model_json)

    # next fib should fail, it should be 3 since there are 2 descriptors
    model_to_validate = {
        "name": "character",
        "descriptors": ["1", "1.0"],
        "next_fib": 8,
        "level_up": True,
        "strict": True
    }

    model_json = json.dumps(model_to_validate)
    with pytest.raises(errors.SeedValidationException):
        model_to_validate = Asset.model_validate_json(model_json)


    # All sorts of wrong should be auto-fixed based on number of descriptors
    name = "ChArAcTeR"
    descriptors = ["1", "1.0","Light","foRce"]
    model_to_validate = {
        "name": name, # case issues
        "descriptors": descriptors,  # Non Fib number, case issues
        "next_fib": 11, # next_fib should be 5 based on number of descriptors
        "level_up": True, # level_up should be false since number of descriptors isn't a Fib number'
        "strict": False
    }
    model_json = json.dumps(model_to_validate)
    model_to_validate = Asset.model_validate_json(model_json)

    assert model_to_validate.next_fib == 5
    assert not model_to_validate.level_up
    assert model_to_validate.num_descriptors == 4
    assert model_to_validate.name == name.lower()
    assert len([i for i in descriptors if i.lower() in model_to_validate.descriptors]) == len(descriptors)