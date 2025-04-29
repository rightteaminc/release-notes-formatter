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
    return Path(__file__).parent / "fixtures" / "sample_ui_release_notes.md"

@pytest.fixture
def parser():
    return ReleaseNoteParser()

def test_parse_sections(parser, sample_release_notes):
    """Test that all sections are correctly identified from the markdown file."""
    entries = parser.parse_file(sample_release_notes)
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
    
    ticket_ids = {
        entry.ticket_id 
        for entry in entries 
        if entry.entry_type == EntryType.AZURE_TICKET
    }
    
    assert ticket_ids == {9396, 9423, 9460, 9264, 9283, 9416, 9111, 9347, 8752, 9364, 9387}

def test_duplicate_entries(parser, sample_release_notes):
    """Test that duplicate entries are properly handled and appear in multiple sections."""
    entries = parser.parse_file(sample_release_notes)
    
    ticket_9396_entries = [
        entry for entry in entries 
        if entry.entry_type == EntryType.AZURE_TICKET 
        and entry.ticket_id == 9396
    ]
    
    sections_for_9396 = {entry.section for entry in ticket_9396_entries}
    assert sections_for_9396 == {"🏷 Enhancements", "Requires Feature Flag"}
    assert len(ticket_9396_entries) == 2

def test_non_ticket_entries(parser, sample_release_notes):
    """Test that non-ticket entries are properly parsed."""
    entries = parser.parse_file(sample_release_notes)
    
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
    (
        "- [1234](https://dev.azure.com/...) - Create new Pagination Model in the Public API Project",
        EntryType.WORK_ITEM,
        {"ticket_id": 1234, "title": "Create new Pagination Model in the Public API Project"}
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
    
    renovate_entry = next(
        entry for entry in entries
        if entry.author == "renovate[bot]"
    )
    
    assert renovate_entry.entry_type == EntryType.DEPENDENCY_UPDATE
    assert renovate_entry.title == "Update all non-major dependencies"
    
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
    
    dependency_entries = [
        entry for entry in entries
        if entry.entry_type == EntryType.DEPENDENCY_UPDATE
    ]
    
    assert len(dependency_entries) == 4

    titles = {entry.title for entry in dependency_entries}
    
    assert "dependencies/remove-auto-sizer-types" in titles
    assert "Update all non-major dependencies" in titles
    assert "removes deprecated dependencies" in titles
    
    additional_entries = [
        "- Update package versions @maintainer (#101)",
        "- Fix dependencies issue @developer (#102)",
        "- Regular feature @user (#103)"  # Non-dependency entry
    ]
    
    results = [parser.parse_line(entry) for entry in additional_entries]
    
    assert all(results), "All entries should be parsed successfully"
    assert [r.entry_type for r in results] == [
        EntryType.DEPENDENCY_UPDATE,   # Contains "Update"
        EntryType.DEPENDENCY_UPDATE,   # Contains "dependencies"
        EntryType.CUSTOM               # No dependency-related keywords
    ]

def test_parse_file_with_be_work_items(tmp_path):
    """Test parsing a file with BE work item entries."""
    content = """
## Work Items
- [9176](https://dev.azure.com/...) - Create new Pagination Model in the Public API Project
- [9569](https://dev.azure.com/...) - Public Clients Endpoints returning 500 responses
    """

    filepath = tmp_path / "be_work_items.md"

    filepath.write_text(content)
    
    parser = ReleaseNoteParser()
    entries = parser.parse_file(str(filepath))

    assert len(entries) == 2
    assert all(e.entry_type == EntryType.WORK_ITEM for e in entries)
    assert entries[0].ticket_id == 9176
    assert entries[0].title == "Create new Pagination Model in the Public API Project"
    assert entries[1].ticket_id == 9569
    assert entries[1].title == "Public Clients Endpoints returning 500 responses"

def test_parse_file_with_blank_lines(tmp_path):
    """Test parse_file with a file containing only blank lines."""
    content = """
    
    
    """
    
    filepath = tmp_path / "blank_lines.md"
    
    filepath.write_text(content)
    
    parser = ReleaseNoteParser()
    entries = parser.parse_file(str(filepath))

    assert entries == []

def test_parse_file_with_only_section_headers(tmp_path):
    """Test parse_file with a file containing only section headers."""
    content = """
    ## Section 1
    ## Section 2
    """

    filepath = tmp_path / "only_sections.md"
    
    filepath.write_text(content)
    
    parser = ReleaseNoteParser()
    entries = parser.parse_file(str(filepath))
    
    assert entries == []

def test_parse_file_with_only_malformed_lines(tmp_path):
    """Test parse_file with a file containing only malformed lines."""
    content = """
    - This is not a valid entry
    - [AB#](...) - Missing ticket ID @user (#123)
    - [] - Empty ticket @user (#123)
    """

    filepath = tmp_path / "malformed_lines.md"
    
    filepath.write_text(content)
    
    parser = ReleaseNoteParser()
    entries = parser.parse_file(str(filepath))
    assert entries == []

def test_parse_file_with_dependency_section(tmp_path):
    """Test parse_file with a dependency section and a dependency entry."""
    content = """
    ## 🧩 Dependencies
    - Update all non-major dependencies @renovate[bot] (#5678)
    """

    filepath = tmp_path / "dependency_section.md"
    
    filepath.write_text(content)

    parser = ReleaseNoteParser()
    entries = parser.parse_file(str(filepath))
    
    assert len(entries) == 1
    assert entries[0].entry_type == EntryType.DEPENDENCY_UPDATE
    assert entries[0].section == "🧩 Dependencies"

def test_invalid_non_azure_entry():
    """Test that a non-azure entry with missing PR number raises InvalidEntryFormatError."""
    
    parser = ReleaseNoteParser()
    
    with pytest.raises(InvalidEntryFormatError):
        parser.parse_line("- custom/change @user ()")

def test_extract_author_renovate_bot():
    parser = ReleaseNoteParser()
    
    import re
    
    line = "- Update all non-major dependencies @[renovate[bot]](https://github.com/apps/renovate) (#1234)"
    pattern = re.compile(r"- (.*?) @(\[renovate\[bot\]\]\(https://github.com/apps/renovate\)) \(#(\d+)\)")
    match = pattern.match(line)
    author = parser._extract_author(match, author_group_start=2)
    
    assert author == "renovate[bot]"

def test_extract_author_markdown_link():
    parser = ReleaseNoteParser()

    
    import re
    
    line = "- Custom change @[user](https://github.com/user) (#1234)"
    pattern = re.compile(r"- (.*?) @\[(.*?)\]\(.*?\) \(#(\d+)\)")
    match = pattern.match(line)
    author = parser._extract_author(match, author_group_start=2)
    
    assert author == "user"

def test_create_azure_entry_index_error():
    parser = ReleaseNoteParser()
    
    import re
    
    # Missing PR number group
    line = "- [AB#1234](...) - Test @user"
    pattern = re.compile(r"- \[AB#(\d+)\]\(.*?\) - (.*?) @(\S+)")
    match = pattern.match(line)
    
    try:
        parser._create_azure_entry(line, match)
    except Exception as e:
        assert isinstance(e, InvalidEntryFormatError)

def test_create_non_azure_entry_index_error():
    parser = ReleaseNoteParser()

    import re
    
    # Missing PR number group
    line = "- Custom change @user"
    pattern = re.compile(r"- (.*?) @(\S+)")
    match = pattern.match(line)
    
    try:
        parser._create_non_azure_entry(line, match)
    except Exception as e:
        assert isinstance(e, InvalidEntryFormatError)

def test_dependency_entry_in_non_dependency_section(tmp_path):
    content = """
    ## 🏷 Enhancements
    - Update all non-major dependencies @renovate[bot] (#5678)
    """

    filepath = tmp_path / "non_dep_section.md"
    
    filepath.write_text(content)
    
    parser = ReleaseNoteParser()
    entries = parser.parse_file(str(filepath))
    
    assert len(entries) == 1
    # Should be marked as dependency due to keyword, not section
    assert entries[0].entry_type == EntryType.DEPENDENCY_UPDATE
    assert entries[0].section == "🏷 Enhancements" 