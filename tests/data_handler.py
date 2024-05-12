import json
import os
import pytest
from utils.data_handler import load_existing_data

@pytest.fixture
def test_filename():
    return 'test_data/test_url_data.json'

@pytest.fixture
def test_data():
    return [
        {'url': 'https://example.com', 'status_code': 200},
        {'url': 'https://example.org', 'status_code': 301},
    ]

def test_load_existing_data_file_exists(test_filename, test_data):
    # Create a test JSON file with sample data
    os.makedirs(os.path.dirname(test_filename), exist_ok=True)
    with open(test_filename, 'w') as file:
        json.dump(test_data, file)

    # Call the load_existing_data function
    existing_urls = load_existing_data(test_filename)

    # Assert that the existing URLs are loaded correctly
    expected_urls = {'https://example.com', 'https://example.org'}
    assert existing_urls == expected_urls

    # Clean up the test JSON file
    os.remove(test_filename)

def test_load_existing_data_file_not_exists(test_filename):
    # Ensure the test JSON file doesn't exist
    if os.path.exists(test_filename):
        os.remove(test_filename)

    # Call the load_existing_data function
    existing_urls = load_existing_data(test_filename)

    # Assert that an empty set is returned
    assert existing_urls == set()

    # Assert that the data directory and JSON file are created
    assert os.path.exists(os.path.dirname(test_filename))
    assert os.path.exists(test_filename)

    # Clean up the test JSON file
    os.remove(test_filename)