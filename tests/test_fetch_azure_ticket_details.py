"""
Tests for Azure ticket fetcher functionality (new workflow).

This module tests the functionality for fetching Azure ticket details for a list of ticket IDs.
"""

import pytest
from unittest.mock import patch
import yaml
from fetch_azure_ticket_details import fetch_work_items

@patch('fetch_azure_ticket_details.requests.get')
def test_fetch_work_items_with_ticket_ids(mock_get):
    """Test fetching Azure ticket details for a list of ticket IDs."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "fields": {
            "System.Title": "Mock Title",
            "System.Description": "Mock Description"
        }
    }
    ticket_ids = [1234, 5678]
    results = fetch_work_items(ticket_ids)
    assert len(results) == 2
    for i, entry in enumerate(results):
        assert entry["id"] == str(ticket_ids[i]) or entry["id"] == ticket_ids[i]
        assert entry["title"] == "Mock Title"
        assert entry["description"] == "Mock Description"

    # Test YAML output
    yaml_str = yaml.dump(results)
    assert "Mock Title" in yaml_str
    assert "Mock Description" in yaml_str 