import json
import pytest

from pydantic_core import from_json
from seed.models import Asset
from seed import common

pytestmark = pytest.mark.asset

@pytest.fixture(scope="session")
def basic_asset_dict(basic_asset_json):
    obj = json.loads(basic_asset_json)
    yield obj

@pytest.fixture(scope="session")
def basic_asset_hashtags(basic_asset_dict):
    yield basic_asset_dict["descriptors"]

@pytest.fixture(scope="session")
def basic_asset(basic_asset_json):
    yield Asset.model_validate_json(basic_asset_json)

def test_basic_asset(basic_asset, basic_asset_dict):
    """ Validate the values from the basic json file. """

    # Attribute Validations
    assert basic_asset.name == basic_asset_dict["name"]
    assert basic_asset.next_fib == basic_asset_dict["next_fib"]
    assert basic_asset.level_up == False
    assert basic_asset.descriptors == {"1","1.0"}

def test_basic_asset_hashtags(basic_asset, basic_asset_hashtags):
    valid_hastags = ["desc1", "desc2"]
    # Validate the hashtags used in the json file
    for i in basic_asset.hashtags:
        assert i in basic_asset_hashtags

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
