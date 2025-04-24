"""
Tests for Azure ticket fetcher functionality.

This module tests the functionality for fetching and processing both Azure and non-Azure entries.
"""

import pytest
from unittest.mock import patch, Mock
from pathlib import Path
import yaml

from release_notes.models import ReleaseNoteEntry, EntryType
from fetch_azure_ticket_details import parse_release_notes, fetch_work_items

@pytest.fixture
def mock_entries():
    """Create a mix of Azure and non-Azure entries for testing."""
    return [
        ReleaseNoteEntry(
            raw_text="- [AB#1234](...) - Azure ticket @user (#100)",
            entry_type=EntryType.AZURE_TICKET,
            section="🏷 Enhancements",
            ticket_id=1234,
            title="Azure ticket",
            author="user",
            pr_number="100"
        ),
        ReleaseNoteEntry(
            raw_text="- Update all non-major dependencies @renovate[bot] (#200)",
            entry_type=EntryType.DEPENDENCY_UPDATE,
            section="🧩 Dependencies",
            ticket_id=None,
            title="Update all non-major dependencies",
            author="renovate[bot]",
            pr_number="200"
        ),
        ReleaseNoteEntry(
            raw_text="- Custom change @user (#300)",
            entry_type=EntryType.CUSTOM,
            section="🏷 Enhancements",
            ticket_id=None,
            title="Custom change",
            author="user",
            pr_number="300"
        )
    ]

@pytest.fixture
def mock_azure_response():
    """Mock Azure API response for ticket data."""
    return {
        "fields": {
            "System.Title": "Azure API Title",
            "System.Description": "Azure API Description"
        }
    }

def test_parse_release_notes_with_mixed_entries(tmp_path, mock_entries):
    """Test parsing a file with both Azure and non-Azure entries."""
    content = """
## 🏷 Enhancements
- [AB#1234](...) - Azure ticket @user (#100)
- Custom change @user (#300)

## 🧩 Dependencies
- Update all non-major dependencies @renovate[bot] (#200)
"""
    test_file = tmp_path / "test_notes.md"
    test_file.write_text(content)

    entries = parse_release_notes(str(test_file))
    
    assert len(entries) == 3, "Should include all entry types, not just Azure tickets"
    
    # Verify each type of entry is included
    entry_types = {entry.entry_type for entry in entries}
    assert EntryType.AZURE_TICKET in entry_types, "Should include Azure tickets"
    assert EntryType.DEPENDENCY_UPDATE in entry_types, "Should include dependency updates"
    assert EntryType.CUSTOM in entry_types, "Should include custom entries"

@patch('fetch_azure_ticket_details.requests.get')
def test_fetch_work_items_with_mixed_entries(mock_get, mock_entries, mock_azure_response):
    """Test processing both Azure and non-Azure entries."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_azure_response

    result = fetch_work_items(mock_entries)

    assert len(result) == 3, "Should include all entry types"
    
    # Verify Azure entry
    azure_entry = next(e for e in result if e["entry_type"] == "azure_ticket")
    assert azure_entry["ticket_id"] == 1234
    assert azure_entry["azure_title"] == "Azure API Title"
    assert azure_entry["azure_description"] == "Azure API Description"
    
    # Verify dependency entry
    dep_entry = next(e for e in result if e["entry_type"] == "dependency_update")
    assert dep_entry["title"] == "Update all non-major dependencies"
    assert dep_entry["author"] == "renovate[bot]"
    assert "azure_title" not in dep_entry
    
    # Verify custom entry
    custom_entry = next(e for e in result if e["entry_type"] == "custom")
    assert custom_entry["title"] == "Custom change"
    assert custom_entry["author"] == "user"
    assert "azure_title" not in custom_entry

@patch('fetch_azure_ticket_details.requests.get')
def test_yaml_output_format_with_mixed_entries(mock_get, tmp_path, mock_entries, mock_azure_response):
    """Test the YAML output format with mixed entry types."""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_azure_response

    result = fetch_work_items(mock_entries)

    output_file = tmp_path / "test_output.yml"
    with open(output_file, "w") as f:
        yaml.dump(result, f)

    with open(output_file) as f:
        yaml_content = yaml.safe_load(f)

    assert len(yaml_content) == 3, "Should include all entry types in YAML output"
    
    entry_types = {entry["entry_type"] for entry in yaml_content}
    assert "azure_ticket" in entry_types
    assert "dependency_update" in entry_types
    assert "custom" in entry_types
    
    # Verify Azure-specific fields only appear in Azure entries
    for entry in yaml_content:
        if entry["entry_type"] == "azure_ticket":
            assert "azure_title" in entry
            assert "azure_description" in entry
        else:
            assert "azure_title" not in entry
            assert "azure_description" not in entry 