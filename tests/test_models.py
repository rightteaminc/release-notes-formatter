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