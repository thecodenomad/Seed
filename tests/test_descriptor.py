import json
import pytest

from pydantic_core import from_json
from seed import errors, common
from seed.models import Descriptor

pytestmark = pytest.mark.descriptor

@pytest.fixture(scope="function")
def basic_descriptor_dict(basic_descriptor_json):
    obj = json.loads(basic_descriptor_json)
    yield obj

@pytest.fixture(scope="function")
def basic_descriptor_descriptions(basic_descriptor_dict):
    yield basic_descriptor_dict["descriptions"]

@pytest.fixture(scope="function")
def basic_descriptor(basic_descriptor_json):
    desc = Descriptor.model_validate_json(basic_descriptor_json)
    assert desc.descriptions is not None
    yield desc

#########
# Tests #
#########

def test_add_description(basic_descriptor, basic_descriptor_dict):
    """Test adding a description to a descriptor."""
    assert basic_descriptor.next_fib == basic_descriptor_dict["next_fib"]

    # Validate next_fib increase
    test_values = [("red", 2), ("WhItE", 3), ("Blue hair", 5)]
    for desc, fib in test_values:
        basic_descriptor.add_description(desc)

        # The description should be all lowercase
        assert desc.lower() in basic_descriptor.descriptions
        assert basic_descriptor.next_fib == fib
        assert basic_descriptor.level_up

def test_level_up():
    """Test adding descriptions to a descriptor."""

    basic_descriptor = Descriptor(name="snarky_snark")
    descriptions     = [("1", 2),("2", 3),("3", 5),("4",5),("5",8),("6",8),("7",8)]

    for description, fib in descriptions:
        next_fib = basic_descriptor.next_fib
        basic_descriptor.add_description(description)
        assert basic_descriptor.next_fib == fib

        fib_check = common.is_fibonacci(basic_descriptor.num_descriptions)
        assert basic_descriptor.level_up == fib_check
        assert basic_descriptor.is_uneven() is not fib_check

def test_descriptor_sharing(basic_descriptor):
    test_first_asset_name = "character1"
    test_second_asset_name = "setting1"

    basic_descriptor.link_asset(test_first_asset_name)
    assert not basic_descriptor.is_multi_asset_linked()

    # Add again and validate that the set is doing it's thang
    basic_descriptor.link_asset(test_first_asset_name)
    assert not basic_descriptor.is_multi_asset_linked()

    basic_descriptor.link_asset(test_second_asset_name)
    assert basic_descriptor.is_multi_asset_linked()

    basic_descriptor.remove_link(test_first_asset_name)
    assert not basic_descriptor.is_multi_asset_linked()

    # All links removed
    basic_descriptor.remove_link(test_second_asset_name)
    assert not basic_descriptor.is_multi_asset_linked()
    assert basic_descriptor.is_dangling()

def test_remove_description(basic_descriptor, basic_descriptor_dict):

    # There are 0 descriptions at this point
    assert basic_descriptor.next_fib == basic_descriptor_dict["next_fib"]
    assert basic_descriptor.next_fib == 1

    # Add first description (0 or 1 descriptors returns 2 for Fib(n))
    basic_descriptor.add_description("red")
    assert "red" in basic_descriptor.descriptions
    assert basic_descriptor.next_fib == 2

    # Remove description
    basic_descriptor.remove_description("red")
    assert "red" not in basic_descriptor.descriptions
    assert basic_descriptor.next_fib == 1

def test_invalid_level_up():
    # Level up should fail because the number of descriptors is indeed a Fibonacci number
    model_to_validate = {
        "name": "descriptor",
        "descriptions": ["1", "1.0"],
        "next_fib": 3,
        "level_up": False,
        "strict": True
    }

    model_json = json.dumps(model_to_validate)
    with pytest.raises(errors.SeedValidationException):
        model_to_validate = Descriptor.model_validate_json(model_json)

def test_invalid_next_fib():
    # next fib should fail, it should be 3 since there are 2 descriptors
    model_to_validate = {
        "name": "descriptor",
        "descriptions": ["1", "1.0"],
        "next_fib": 8,
        "level_up": True,
        "strict": True
    }

    model_json = json.dumps(model_to_validate)
    with pytest.raises(errors.SeedValidationException):
        model_to_validate = Descriptor.model_validate_json(model_json)

def test_invalid_description_length():
    # Description length failure since it's not a fibonacci number'
    model_to_validate = {
        "name": "descriptor",
        "descriptions": ["1","1 2","3 5 6 7"],
        "next_fib": 5,
        "level_up": True,
        "strict": True
    }

    model_json = json.dumps(model_to_validate)
    with pytest.raises(errors.FailedDescriptionLength):
        model_to_validate = Descriptor.model_validate_json(model_json)

def test_non_strict():
    # All sorts of wrong should be auto-fixed based on number of descriptors
    name = "DeScRiPtOr"
    descriptions = ["1", "1.0","Light","foRce"]
    model_to_validate = {
        "name": name, # case issues
        "descriptions": descriptions,  # Non Fib number, case issues
        "next_fib": 11, # next_fib should be 5 based on number of descriptors
        "level_up": False, # level_up should be false since number of descriptors isn't a Fib number'
        "strict": False
    }
    model_json = json.dumps(model_to_validate)
    model_to_validate = Descriptor.model_validate_json(model_json)

    assert model_to_validate.next_fib == 5
    assert not model_to_validate.level_up
    assert model_to_validate.num_descriptions == 4
    assert model_to_validate.name == name.lower()
    assert len([i for i in descriptions if i.lower() in model_to_validate.descriptions]) == len(descriptions)
