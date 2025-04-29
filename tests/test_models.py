"""
Tests for the release notes models.

This module contains tests for the data models used in the release notes parser.
"""

import pytest
from release_notes.models import ReleaseNoteEntry, EntryType

def test_release_note_entry_creation():
    """Test basic creation of a ReleaseNoteEntry."""
    entry = ReleaseNoteEntry(
        raw_text="test",
        entry_type=EntryType.AZURE_TICKET,
        ticket_id=1234,
        title="Test Title",
        author="user",
        pr_number=5678
    )
    assert entry.ticket_id == 1234
    assert entry.title == "Test Title"
    assert entry.entry_type == EntryType.AZURE_TICKET

def test_release_note_entry_optional_fields():
    """Test that optional fields can be None."""
    entry = ReleaseNoteEntry(
        raw_text="test",
        entry_type=EntryType.CUSTOM
    )
    assert entry.ticket_id is None
    assert entry.title is None

def test_load_repositories_from_yaml(tmp_path):
    from release_notes.file_utils import load_repositories_from_yaml
    yaml_content = """
repositories:
  - repo1
  - repo2
"""
    yaml_file = tmp_path / "repos.yml"
    yaml_file.write_text(yaml_content)
    repos = load_repositories_from_yaml(str(yaml_file))
    assert repos == ["repo1", "repo2"]

    # Test with missing 'repositories' key
    yaml_file.write_text("other_key: []")
    repos = load_repositories_from_yaml(str(yaml_file))
    assert repos == [] 