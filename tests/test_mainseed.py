import json
import pytest

from pydantic_core import from_json
from seed.models import MainSeed
from seed import common, errors

pytestmark = pytest.mark.asset

@pytest.fixture(scope="session")
def test_seed_dict(basic_json):
    obj = json.loads(basic_json)
    yield obj

@pytest.fixture(scope="session")
def test_seed(basic_json):
    yield MainSeed.model_validate_json(basic_json)


def test_asset(test_seed:MainSeed, test_seed_dict:dict):
    # Test for descriptors
    for desc_name, _ in test_seed_dict["global_descriptors"].items():
        # Assert each name from json file / dict exists
        assert test_seed.global_descriptors.get(desc_name)
    assert test_seed.global_desc_level_up == test_seed_dict["global_desc_level_up"]
    assert test_seed.global_desc_next_fib == test_seed_dict["global_desc_next_fib"]


    # Test for Assets
    for asset_name,_ in test_seed_dict["global_assets"].items():
        # Assert each name from json file / dict exists
        assert test_seed.global_assets.get(asset_name)
    assert test_seed.global_assets_level_up == test_seed_dict["global_assets_level_up"]
    assert test_seed.global_assets_next_fib == test_seed_dict["global_assets_next_fib"]

def test_add_description():
    descriptor_name = "soldier"
    asset_name = "Billy"
    description = "middle-aged"

    _test_seed = MainSeed()

    # Verify doesn't exist'
    assert not _test_seed.global_assets.get(asset_name)
    assert not _test_seed.global_descriptors.get(descriptor_name)

    # Add an asset
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name=descriptor_name, description=description)

    # Test adding the same asset, nothing should happen
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name=descriptor_name, description=description)


    # Verify it exists
    assert _test_seed.global_assets.get(asset_name)
    assert _test_seed.global_descriptors.get(descriptor_name)

    assert description in _test_seed.global_descriptors[descriptor_name].descriptions

def test_invalid_description(test_seed:MainSeed):
    descriptor_name = "desert"
    asset_name = "phoenix"
    description = "this is not fibonacci num in length"

    with pytest.raises(errors.FailedDescriptionLength):
        test_seed.add_description_to_asset(asset_name=asset_name,
            descriptor_name=descriptor_name, description=description)
