import pytest

from pydantic_core import from_json
from seed.models import Asset

pytestmark = pytest.mark.asset

def test_just_asset(basic_asset_json):
    Asset.model_validate_json(basic_asset_json)


#def
