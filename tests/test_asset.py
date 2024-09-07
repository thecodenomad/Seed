import json
import pytest

from pydantic_core import from_json
from seed.models import Asset
from seed import common

pytestmark = pytest.mark.asset

@pytest.fixture(scope="function")
def basic_asset_dict(basic_asset_json):
    obj = json.loads(basic_asset_json)
    yield obj

@pytest.fixture(scope="function")
def basic_asset_hashtags(basic_asset_dict):
    yield basic_asset_dict["descriptors"].keys()

@pytest.fixture(scope="function")
def basic_asset(basic_asset_json):
    yield Asset.model_validate_json(basic_asset_json)

def test_basic_asset(basic_asset, basic_asset_dict):
    """ Validate the values from the basic json file. """

    # Attribute Validations
    assert basic_asset.name == basic_asset_dict["name"]
    assert basic_asset.next_fib == basic_asset_dict["next_fib"]
    assert basic_asset.level_up == False
    assert len(basic_asset.shared_descriptors) == 0

    # Method Validations for basic asset
    assert not basic_asset.has_asset_relation()

def test_basic_asset_hashtags(basic_asset, basic_asset_hashtags):
    valid_hastags = ["desc1", "desc2"]
    # Validate the hashtags used in the json file
    for i in basic_asset.hashtags:
        assert i in basic_asset_hashtags

def test_basic_asset_add_description(basic_asset, basic_asset_dict):
    test_hashtag = "desc3"
    test_description = "blue"

    basic_asset.add_description(test_hashtag, test_description)
    assert basic_asset.descriptors.get(test_hashtag)
    assert test_description in basic_asset.descriptors[test_hashtag].descriptions
    assert basic_asset.next_fib == common.get_next_fibonacci(basic_asset_dict["next_fib"])

def test_basic_asset_add_to_exiting_hashtag(basic_asset, basic_asset_dict):
    test_hashtag = "desc2"
    test_description = "red"
    curr_next_fib = basic_asset.descriptors[test_hashtag].next_fib

    basic_asset.add_description(test_hashtag, test_description)
    assert basic_asset.descriptors.get(test_hashtag)
    assert test_description in basic_asset.descriptors[test_hashtag].descriptions

    # Check descriptor next fib
    # TODO: Move to descriptor test
    to_check_fib = common.get_next_fibonacci(curr_next_fib)
    assert basic_asset.descriptors[test_hashtag].next_fib == to_check_fib
