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

    # Add a few more to hit fibonacci values should be at 2

    # 2 objects
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name="desc-test-1",
        description="test")
    assert _test_seed.global_desc_next_fib == 3

    # 3 objects
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name="desc-test-2",
        description="test")
    assert _test_seed.global_desc_next_fib == 5

    # 4 objects
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name="desc-test-3",
        description="test")

    assert _test_seed.global_desc_next_fib == 5

    # 5 objects
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name="desc-test-4",
        description="test")

    assert _test_seed.global_desc_next_fib == 8


def test_invalid_description(test_seed:MainSeed):
    descriptor_name = "desert"
    asset_name = "phoenix"
    description = "this is not fibonacci num in length"

    with pytest.raises(errors.FailedDescriptionLength):
        test_seed.add_description_to_asset(asset_name=asset_name,
            descriptor_name=descriptor_name, description=description)

def test_asset_relations(test_seed:MainSeed, test_seed_dict:dict):
    asset_one_name = list(test_seed_dict["global_assets"].keys())[0]
    asset_two_name = list(test_seed_dict["global_assets"].keys())[1]
    desc_one_name = list(test_seed_dict["global_descriptors"].keys())[0]
    desc_two_name = list(test_seed_dict["global_descriptors"].keys())[1]

    # Validate no relations prior
    for i in [asset_one_name, asset_two_name]:
        assert len(test_seed.asset_relations(i)) == 0

    # Should be dangling since it hasn't been linked to an asset'
    assert test_seed.global_descriptors[desc_one_name].is_dangling()

    # Should not be multi asset linked yet, but is no longer dangling
    test_seed.link_descriptor(asset_one_name, desc_one_name)
    assert not test_seed.global_descriptors[desc_one_name].is_multi_asset_linked()
    assert not test_seed.global_descriptors[desc_one_name].is_dangling()

    # link the descriptor with another asset
    test_seed.link_descriptor(asset_two_name, desc_one_name)

    # Not dangling because multiple assets are using it
    assert test_seed.global_descriptors[desc_one_name].is_multi_asset_linked()
    assert not test_seed.global_descriptors[desc_one_name].is_dangling()

    a1_relations = test_seed.asset_relations(asset_one_name)
    a2_relations = test_seed.asset_relations(asset_two_name)

    # Validate relationship via desc_one_name
    assert a1_relations[desc_one_name] == asset_two_name
    assert a2_relations[desc_one_name] == asset_one_name

    # The descriptor should have mutiple links now and continue to not be dangling
    assert not test_seed.global_descriptors[desc_one_name].is_dangling()
    assert test_seed.global_descriptors[desc_one_name].is_multi_asset_linked()

    # Test exporting
    test_seed.export_asset_descriptions(asset_one_name)

def test_adding_relation_to_invalid_asset(test_seed:MainSeed):
    # Try searching for relations with an asset that doesn't exist
    with pytest.raises(errors.SeedException):
        test_seed.asset_relations("bogus_asset")

def test_adding_description_to_descriptor(test_seed:MainSeed, test_seed_dict:dict):
    desc_one_name = list(test_seed_dict["global_descriptors"].keys())[0]
    missing_desc_name = "DoesNotExist"

    # Add descriptions
    test_seed.add_description(desc_one_name, "test3 test3 test3")
    test_seed.add_description(missing_desc_name, "test2 test2")

    with pytest.raises(errors.FailedDescriptionLength):
        test_seed.add_description(desc_one_name, "test4 test4 test4 test4")
