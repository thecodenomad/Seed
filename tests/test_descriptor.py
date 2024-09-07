import pytest

from pydantic_core import from_json
from seed.models import Descriptor

pytestmark = pytest.mark.descriptor

def test_descriptor(basic_descriptor_json):
    Descriptor.model_validate_json(basic_descriptor_json)
