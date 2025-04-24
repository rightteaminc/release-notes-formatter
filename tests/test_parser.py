"""
Tests for the release notes parser.

This module contains tests for the parser implementation.
"""

import pytest
from pathlib import Path
from release_notes.parser import ReleaseNoteParser
from release_notes.models import EntryType
from release_notes.exceptions import InvalidEntryFormatError

@pytest.fixture
def sample_release_notes():
    return Path(__file__).parent / "fixtures" / "sample_release_notes.md"

@pytest.fixture
def parser():
    return ReleaseNoteParser()

def test_parse_sections(parser, sample_release_notes):
    """Test that all sections are correctly identified from the markdown file."""
    entries = parser.parse_file(sample_release_notes)
    
    # Get unique sections from entries
    sections = {entry.section for entry in entries}
    
    assert sections == {
        "🏷 Enhancements",
        "🐛 Bug Fixes",
        "🧩 Dependencies",
        "Requires Feature Flag"
    }

def test_azure_ticket_extraction(parser, sample_release_notes):
    """Test that Azure ticket IDs are correctly extracted."""
    entries = parser.parse_file(sample_release_notes)
    
    # Get all unique Azure ticket IDs
    ticket_ids = {
        entry.ticket_id 
        for entry in entries 
        if entry.entry_type == EntryType.AZURE_TICKET
    }
    
    assert ticket_ids == {9396, 9423, 9460, 9264, 9283, 9416, 9111, 9347, 8752, 9364, 9387}

def test_duplicate_entries(parser, sample_release_notes):
    """Test that duplicate entries are properly handled and appear in multiple sections."""
    entries = parser.parse_file(sample_release_notes)
    
    # Find entries for ticket 9396 (appears in Enhancements and Requires Feature Flag)
    ticket_9396_entries = [
        entry for entry in entries 
        if entry.entry_type == EntryType.AZURE_TICKET 
        and entry.ticket_id == 9396
    ]
    
    # Should appear in both Enhancements and Requires Feature Flag
    sections_for_9396 = {entry.section for entry in ticket_9396_entries}
    assert sections_for_9396 == {"🏷 Enhancements", "Requires Feature Flag"}
    assert len(ticket_9396_entries) == 2

def test_non_ticket_entries(parser, sample_release_notes):
    """Test that non-ticket entries are properly parsed."""
    entries = parser.parse_file(sample_release_notes)
    
    # Find dependency entries
    dependency_entries = [
        entry for entry in entries
        if entry.section == "🧩 Dependencies"
    ]
    
    assert len(dependency_entries) == 4
    assert any(
        "remove-auto-sizer-types" in entry.title
        for entry in dependency_entries
    )
    assert any(
        "Update all non-major dependencies" in entry.title
        for entry in dependency_entries
    )

def test_entry_attributes(parser, sample_release_notes):
    """Test that entries contain all expected attributes."""
    entries = parser.parse_file(sample_release_notes)
    
    # Find a specific Azure ticket entry
    timesheet_entry = next(
        entry for entry in entries
        if entry.entry_type == EntryType.AZURE_TICKET
        and entry.ticket_id == 9264
        and entry.section == "🏷 Enhancements"
    )
    
    assert timesheet_entry.title == "Timesheet Search - Add clear icon"
    assert timesheet_entry.author == "kcvikander"
    assert timesheet_entry.pr_number == "9777"

@pytest.mark.parametrize("invalid_entry", [
    "- [AB#](...) - Missing ticket ID @user (#123)",
    "- [AB#abc](...) - Non-numeric ticket ID @user (#123)",
    "- [AB#123](...) - Missing PR number @user",
    "- [AB#123](...) - Invalid PR format @user (#abc)",
    "- [] - Empty ticket @user (#123)",
    "- Missing everything",
])
def test_invalid_azure_entries(invalid_entry):
    """Test that invalid Azure ticket entries raise appropriate errors."""
    parser = ReleaseNoteParser()
    with pytest.raises(InvalidEntryFormatError):
        parser.parse_line(invalid_entry)

@pytest.mark.parametrize("invalid_entry", [
    "- Update all non-major dependencies @renovate[bot] (missing_hash)",
    "- Update all non-major dependencies @renovate[bot] (#abc)",
    "- Update all non-major dependencies (no_author)",
])
def test_invalid_dependency_entries(invalid_entry):
    """Test that invalid dependency entries raise appropriate errors."""
    parser = ReleaseNoteParser()
    with pytest.raises(InvalidEntryFormatError):
        parser.parse_line(invalid_entry)

@pytest.mark.parametrize("entry,expected_type,expected_attrs", [
    (
        "- [AB#1234](...) - Test @user (#5678)", 
        EntryType.AZURE_TICKET,
        {"ticket_id": 1234, "title": "Test", "author": "user", "pr_number": "5678"}
    ),
    (
        "- Update all non-major dependencies @renovate[bot] (#5678)",
        EntryType.DEPENDENCY_UPDATE,
        {"title": "Update all non-major dependencies", "pr_number": "5678"}
    ),
    (
        "- custom/change @user (#5678)",
        EntryType.CUSTOM,
        {"title": "custom/change", "author": "user", "pr_number": "5678"}
    ),
])
def test_entry_variations(entry, expected_type, expected_attrs):
    """Test various valid entry formats with different attributes."""
    parser = ReleaseNoteParser()
    result = parser.parse_line(entry)
    
    assert result.entry_type == expected_type
    for attr, value in expected_attrs.items():
        assert getattr(result, attr) == value

def test_parse_file_with_mixed_entries(tmp_path):
    """Test parsing a file with mixed entry types and invalid lines."""
    content = """
## Section Title
- [AB#1234](...) - Valid ticket @user (#5678)
Some random text that should be ignored
- Update all non-major dependencies @renovate[bot] (#9012)
- custom/entry @author (#3456)
- Invalid entry that should be skipped
    """
    
    filepath = tmp_path / "test_notes.md"
    filepath.write_text(content)
    
    parser = ReleaseNoteParser()
    entries = parser.parse_file(str(filepath))
    
    assert len(entries) == 3
    assert [e.entry_type for e in entries] == [
        EntryType.AZURE_TICKET,
        EntryType.DEPENDENCY_UPDATE,
        EntryType.CUSTOM
    ]

def test_github_style_author_links(parser, sample_release_notes):
    """Test that GitHub-style author links are properly parsed."""
    entries = parser.parse_file(sample_release_notes)
    
    # Find the renovate[bot] entry from the sample file
    renovate_entry = next(
        entry for entry in entries
        if entry.author == "renovate[bot]"
    )
    
    assert renovate_entry.entry_type == EntryType.DEPENDENCY_UPDATE
    assert renovate_entry.title == "Update all non-major dependencies"
    
    # Test additional GitHub-style links
    additional_entries = [
        "- [AB#1234](...) - Test @[developer](https://github.com/developer) (#100)",
        "- Custom change @[designer](https://github.com/designer) (#102)"
    ]
    
    results = [parser.parse_line(entry) for entry in additional_entries]
    
    assert all(results), "All entries should be parsed successfully"
    assert [r.author for r in results] == ["developer", "designer"]
    assert [r.entry_type for r in results] == [
        EntryType.AZURE_TICKET,
        EntryType.CUSTOM
    ]

def test_smart_dependency_detection(parser, sample_release_notes):
    """Test that dependency-related entries are properly categorized."""
    entries = parser.parse_file(sample_release_notes)
    
    # Get all dependency entries
    dependency_entries = [
        entry for entry in entries
        if entry.entry_type == EntryType.DEPENDENCY_UPDATE
    ]
    
    # Verify the known dependency entries from sample file
    assert len(dependency_entries) == 4
    titles = {entry.title for entry in dependency_entries}
    assert "dependencies/remove-auto-sizer-types" in titles
    assert "Update all non-major dependencies" in titles
    assert "removes deprecated dependencies" in titles
    
    # Test additional dependency-related entries
    additional_entries = [
        "- Update package versions @maintainer (#101)",
        "- Fix dependencies issue @developer (#102)",
        "- Regular feature @user (#103)"  # Non-dependency entry
    ]
    
    results = [parser.parse_line(entry) for entry in additional_entries]
    
    assert all(results), "All entries should be parsed successfully"
    assert [r.entry_type for r in results] == [
        EntryType.DEPENDENCY_UPDATE,  # Contains "Update"
        EntryType.DEPENDENCY_UPDATE,  # Contains "dependencies"
        EntryType.CUSTOM             # No dependency-related keywords
    ] 