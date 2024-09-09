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

def test_add_description(basic_descriptor, basic_descriptor_dict):
    assert basic_descriptor.next_fib == basic_descriptor_dict["next_fib"]

    # Add first description
    basic_descriptor.add_description("red")
    assert "red" in basic_descriptor.descriptions
    assert basic_descriptor.next_fib == 2

    # Add second description
    basic_descriptor.add_description("white")
    assert "white" in basic_descriptor.descriptions
    assert basic_descriptor.next_fib == 3

    # Add second description
    basic_descriptor.add_description("blue hair")
    assert "blue hair" in basic_descriptor.descriptions
    assert basic_descriptor.next_fib == 5

    with pytest.raises(errors.FailedDescriptionLength):
        # next_fib should be 3, so 2 word description is not allowed
        basic_descriptor.add_description("black shoes in sun")

def test_adding_non_fib_length(basic_descriptor:Descriptor):
    """Test adding descriptions to a descriptor."""

    # At the start of the test, the descriptor doesn't have a description yet
    assert basic_descriptor.next_fib == 1

    verify_next_fibs = [ 2,  3,  5,  5,  8,  8,  8]
    descriptions     = ["1","2","3","4","5","6","7"]
    basic_descriptor.descriptions = []

    for index, description in enumerate(descriptions):
        next_fib = basic_descriptor.next_fib
        basic_descriptor.add_description(description)
        assert basic_descriptor.next_fib == verify_next_fibs[index]

        # Level Up is set whenever the length of the descriptions equals a Fibonacci number
        if common.is_fibonacci(len(basic_descriptor.descriptions)):
            assert basic_descriptor.level_up
            assert not basic_descriptor.is_uneven()
        else:
            assert not basic_descriptor.level_up
            assert basic_descriptor.is_uneven()

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

def test_is_shared(basic_descriptor):

    # Validate no linked / dangling
    assert not basic_descriptor.is_multi_asset_linked()
    assert basic_descriptor.is_dangling()

    # Validate no dangling, 1 asset
    basic_descriptor.link_asset("new-asset")
    assert not basic_descriptor.is_multi_asset_linked()
    assert not basic_descriptor.is_dangling()

    # Validate no dangling, multi asset
    basic_descriptor.link_asset("new-asset-1")
    assert basic_descriptor.is_multi_asset_linked()
    assert not basic_descriptor.is_dangling()

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

def test_validate_descriptions(basic_descriptor_dict:dict):
    desc = "this will not work"
    basic_descriptor_dict["descriptions"] =  [desc]

    json_obj = json.dumps(basic_descriptor_dict)
    with pytest.raises(errors.FailedDescriptionLength):
        # next_fib should be 3, so 2 word description is not allowed
        Descriptor.model_validate_json(json_obj)
