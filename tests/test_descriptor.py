import json
import pytest

from pydantic_core import from_json
from seed import errors
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
    yield Descriptor.model_validate_json(basic_descriptor_json)

def test_add_description(basic_descriptor, basic_descriptor_dict):
    assert basic_descriptor.next_fib == basic_descriptor_dict["next_fib"]

    # Add first description
    basic_descriptor.add_description("red")
    assert "red" in basic_descriptor.descriptions

    # Add second description
    basic_descriptor.add_description("white")
    assert "white" in basic_descriptor.descriptions

    # Add second description
    basic_descriptor.add_description("blue hair")
    assert "blue hair" in basic_descriptor.descriptions

    with pytest.raises(errors.FailedDescriptionLength):
        # next_fib should be 3, so 2 word description is not allowed
        basic_descriptor.add_description("black shoes")

def test_is_shared(basic_descriptor):
    assert not basic_descriptor.is_multi_asset_linked()

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