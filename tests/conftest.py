import json
import os
import pytest

test_folder = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture(scope="session")
def basic_json():
    json_file_path = f"{test_folder}/data/basic.json"

    # Load JSON data from file
    with open(json_file_path, 'r') as file:
        yield file.read()

@pytest.fixture(scope="session")
def basic_descriptor_json():
    json_file_path = f"{test_folder}/data/basic_descriptor.json"

    # Load JSON data from file
    with open(json_file_path, 'r') as file:
        yield file.read()

@pytest.fixture(scope="session")
def basic_asset_json():
    json_file_path = f"{test_folder}/data/basic_asset.json"

    # Load JSON data from file
    with open(json_file_path, 'r') as file:
        yield file.read()
