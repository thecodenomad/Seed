import json
import pytest

from pydantic_core import from_json
from seed.models import MainSeed
from seed import common, errors

pytestmark = pytest.mark.asset

@pytest.fixture(scope="function")
def test_seed_dict(basic_json):
    obj = json.loads(basic_json)
    yield obj

@pytest.fixture(scope="function")
def test_seed(basic_json):
    yield MainSeed.model_validate_json(basic_json)

def test_adding_assets(test_seed_dict:dict):
    test_seed = MainSeed()
    asset_one_name = list(test_seed_dict["global_assets"].keys())[0]

    # There are currently 0 assets, global_asset_next_fib should be 1
    assert test_seed.global_assets_next_fib == 1

    # Add an asset making 1 total
    test_seed._ensure_asset("DoesNotExist-1")
    assert len(test_seed.global_assets) == 1
    assert test_seed.global_assets_next_fib == 2
    assert test_seed.global_assets_level_up

    # Re-add asset nothing should change
    test_seed._ensure_asset("DoesNotExist-1")
    assert len(test_seed.global_assets) == 1
    assert test_seed.global_assets_next_fib == 2
    assert test_seed.global_assets_level_up

    # Add an asset making 2 total
    test_seed._ensure_asset("DoesNotExist-2")
    assert len(test_seed.global_assets) == 2
    assert test_seed.global_assets_next_fib == 3
    assert test_seed.global_assets_level_up

    # Add an asset making 3 total
    test_seed._ensure_asset("DoesNotExist-3")
    assert len(test_seed.global_assets) == 3
    assert test_seed.global_assets_next_fib == 5
    assert test_seed.global_assets_level_up

    # Add an asset making 4 total
    test_seed._ensure_asset("DoesNotExist-4")
    assert len(test_seed.global_assets) == 4
    assert test_seed.global_assets_next_fib == 5
    assert not test_seed.global_assets_level_up

def test_adding_description(test_seed:MainSeed, test_seed_dict:dict):
    desc_one_name = list(test_seed_dict["global_descriptors"].keys())[0]
    missing_desc_name = "DoesNotExist"

    # There are currently 3 descriptors, global_desc_next_fib should be 5
    assert test_seed.global_desc_next_fib == 5

    # Add a description to an existing descriptor with 1 description
    test_seed.add_description(desc_one_name, "test3 test3 test3")
    assert test_seed.global_descriptors[desc_one_name].level_up
    assert test_seed.global_descriptors[desc_one_name].next_fib == 3
    assert len(test_seed.global_descriptors) == 3
    assert test_seed.global_desc_next_fib == 5

    # Add a description with a new descriptor keeping global_desc_next_fib == 5
    test_seed.add_description(missing_desc_name, "test2 test2")
    assert test_seed.global_descriptors[missing_desc_name].level_up
    assert test_seed.global_descriptors[missing_desc_name].next_fib == 2
    assert len(test_seed.global_descriptors) == 4
    assert test_seed.global_desc_next_fib == 5

    # Validate adding a non-Fibonacci number length description
    with pytest.raises(errors.FailedDescriptionLength):
        test_seed.add_description(desc_one_name, "test4 test4 test4 test4")

def test_adding_description_to_asset():
    descriptor_name = "soldier"
    asset_name = "billy"
    description = "middle-aged"

    _test_seed = MainSeed()

    # Verify doesn't exist'
    assert not _test_seed.global_assets.get(asset_name)
    assert not _test_seed.global_descriptors.get(descriptor_name)

    # Add an asset, this will result in a single asset and a single descriptor
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name=descriptor_name, description=description)
    assert _test_seed.global_desc_next_fib == 2
    assert _test_seed.global_assets.get(asset_name)
    assert _test_seed.global_descriptors.get(descriptor_name)
    assert description in _test_seed.global_descriptors[descriptor_name].descriptions

    # Re-add the same asset, nothing should happen
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name=descriptor_name, description=description)
    assert _test_seed.global_desc_next_fib == 2

    # Add an additional descriptor
    _test_seed.add_description_to_asset(asset_name=asset_name,
        descriptor_name="desc-test-1",
        description="test")
    # 2 descriptors at this point
    assert _test_seed.global_desc_next_fib == 3

def test_adding_descriptors(test_seed_dict:dict):
    test_seed = MainSeed()
    desc_one_name = list(test_seed_dict["global_descriptors"].keys())[0]

    # There are currently 0 descriptors, global_desc_next_fib should be 1
    assert test_seed.global_desc_next_fib == 1

    # Add a descriptor making 1 total
    test_seed._ensure_descriptor("DoesNotExist-1")
    assert len(test_seed.global_descriptors) == 1
    assert test_seed.global_desc_next_fib == 2
    assert test_seed.global_desc_level_up

    # Re-add asset nothing should change
    test_seed._ensure_descriptor("DoesNotExist-1")
    assert len(test_seed.global_descriptors) == 1
    assert test_seed.global_desc_next_fib == 2
    assert test_seed.global_desc_level_up

    # Add an asset making 2 total
    test_seed._ensure_descriptor("DoesNotExist-2")
    assert len(test_seed.global_descriptors) == 2
    assert test_seed.global_desc_next_fib == 3
    assert test_seed.global_desc_level_up

    # Add an asset making 3 total
    test_seed._ensure_descriptor("DoesNotExist-3")
    assert len(test_seed.global_descriptors) == 3
    assert test_seed.global_desc_next_fib == 5
    assert test_seed.global_desc_level_up

    # Add an asset making 4 total
    test_seed._ensure_descriptor("DoesNotExist-4")
    assert len(test_seed.global_descriptors) == 4
    assert test_seed.global_desc_next_fib == 5
    assert not test_seed.global_desc_level_up

def test_adding_relation_to_invalid_asset(test_seed:MainSeed):
    # Try searching for relations with an asset that doesn't exist
    with pytest.raises(errors.AssetNotFound):
        test_seed.asset_relations("bogus_asset")

def test_asset_relation(test_seed:MainSeed, test_seed_dict:dict):
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

    # link a dangling descriptor to asset_two
    test_seed.link_descriptor(asset_two_name, desc_two_name)

    a1_relations = test_seed.asset_relations(asset_one_name)
    a2_relations = test_seed.asset_relations(asset_two_name)

    # Validate relationship via desc_one_name
    assert a1_relations[desc_one_name] == asset_two_name
    assert a2_relations[desc_one_name] == asset_one_name

    # The descriptor should have mutiple links now and continue to not be dangling
    assert not test_seed.global_descriptors[desc_one_name].is_dangling()
    assert test_seed.global_descriptors[desc_one_name].is_multi_asset_linked()

def test_exported_asset(test_seed:MainSeed, test_seed_dict:dict):
    asset_one_name = list(test_seed_dict["global_assets"].keys())[0]
    desc_one_name = list(test_seed_dict["global_descriptors"].keys())[0]

    short_description = "TeSt1 TestOne"
    longer_description = "This is a much longer sentence that will demonstrate the fibonacci number usage"

    # 0 descriptions for desc_one_name at this point next_fib == 1
    assert test_seed.global_descriptors[desc_one_name].next_fib == 1

    # 2 descriptions for desc_one_name at this point next_fib == 3
    test_seed.add_description_to_asset(asset_one_name, desc_one_name, short_description)
    assert test_seed.global_descriptors[desc_one_name].next_fib == 3

    # 3 descriptions for desc_one_name at this point next_fib == 5
    test_seed.add_description_to_asset(asset_one_name, desc_one_name, longer_description)
    assert test_seed.global_descriptors[desc_one_name].next_fib == 5

    # Test exporting
    exported_asset = test_seed.export_asset_descriptions(asset_one_name)
    assert short_description.lower() in exported_asset
    assert longer_description.lower() in exported_asset

def test_globals(test_seed:MainSeed, test_seed_dict:dict):
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

def test_invalid_description(test_seed:MainSeed):
    descriptor_name = "desert"
    asset_name = "phoenix"
    description = "this is not fibonacci num in length"

    with pytest.raises(errors.FailedDescriptionLength):
        test_seed.add_description_to_asset(asset_name=asset_name,
            descriptor_name=descriptor_name, description=description)
