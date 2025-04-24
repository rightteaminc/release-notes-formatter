"""Tests for the GitHub release notes formatter module."""

import re
import os
import filecmp
import shutil
import pytest
from pull_and_format_github_release_notes import (
    format_ticket_number_list,
    build_release_item_text,
    format_ticket_number,
    transform_markdown,
    pull_current_draft_release
)

BASE_URL = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'


class TestFormatTicketNumber:
    def test_format_ticket_number_basic(self):
        """Test basic ticket number formatting."""
        match = re.search(r'(\d+)', 'AB#1234')
        expected = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"
        assert format_ticket_number(match, BASE_URL) == expected

    def test_format_ticket_number_with_different_url(self):
        """Test ticket formatting with a different base URL."""
        match = re.search(r'(\d+)', 'AB#5678')
        custom_url = 'https://custom.azure.com/workitems/'
        expected = "[AB#5678](https://custom.azure.com/workitems/5678)"
        assert format_ticket_number(match, custom_url) == expected


class TestFormatTicketNumberList:
    def test_format_ticket_number_list_basic(self):
        """Test basic ticket list formatting."""
        input_string = "- AB#1234 - some context about this pr"
        expected = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"
        match = re.search(r'(?<=- )AB[#-]?(\d+)', input_string)
        assert format_ticket_number_list(match, BASE_URL) == expected

    def test_format_AB_with_hash(self):
        """Test formatting when AB has a hash."""
        input_string = "- AB#1234 - some context about this pr"
        expected = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"
        match = re.search(r'(?<=- )AB[#-]?(\d+)', input_string)
        assert format_ticket_number_list(match, BASE_URL) == expected

    def test_format_AB_with_hyphen(self):
        """Test formatting when AB has a hyphen."""
        input_string = "- AB-1234-some context about this pr"
        expected = "[AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234)"
        match = re.search(r'(?<=- )AB[#-]?(\d+)', input_string)
        assert format_ticket_number_list(match, BASE_URL) == expected


class TestBuildReleaseItemText:
    def test_build_final_content(self):
        """Test building complete release item text."""
        input_string = "- AB#1234 - some context about this pr"
        expected = "- [AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234) - some context about this pr"
        assert build_release_item_text(input_string, BASE_URL) == expected

    def test_no_ticket_in_line(self):
        """Test handling lines without tickets."""
        input_string = "- Just a regular line without a ticket"
        assert build_release_item_text(input_string, BASE_URL) == input_string

    def test_extra_spaces_handling(self):
        """Test handling extra spaces in the input."""
        input_string = "- AB#1234   -    some context about this pr"
        expected = "- [AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234) - some context about this pr"
        assert build_release_item_text(input_string, BASE_URL) == expected


@pytest.fixture
def temp_files(tmp_path):
    """Create temporary input and output files for testing."""
    input_file = tmp_path / "input.md"
    output_file = tmp_path / "output.md"
    mock_content = """# Release Notes
- AB#1234 - Feature one
- AB-5678 - Feature two
"""
    input_file.write_text(mock_content)
    return input_file, output_file


class TestTransformMarkdown:
    def test_transform_markdown_file(self, temp_files):
        """Test transforming a complete markdown file."""
        input_file, output_file = temp_files
        transform_markdown(str(input_file), str(output_file), BASE_URL)
        
        expected_content = """# Release Notes
- [AB#1234](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/1234) - Feature one
- [AB#5678](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/5678) - Feature two
"""
        assert output_file.read_text() == expected_content

    def test_transform_markdown_empty_file(self, tmp_path):
        """Test transforming an empty markdown file."""
        input_file = tmp_path / "empty.md"
        output_file = tmp_path / "output.md"
        input_file.write_text("")
        
        transform_markdown(str(input_file), str(output_file), BASE_URL)
        assert output_file.read_text() == ""


class TestIntegration:
    def test_end_to_end_flow(self, tmp_path, sample_release_notes):
        """Test the complete flow from input to output."""
        input_file = tmp_path / "input.md"
        output_file = tmp_path / "output.md"
        
        with open(sample_release_notes, 'r') as src, open(input_file, 'w') as dest:
            dest.write(src.read())
            
        transform_markdown(str(input_file), str(output_file), BASE_URL)
        
        with open(output_file, 'r') as f:
            content = f.read()
            assert '[AB#9396](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/9396)' in content
            assert '[AB#9423](https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/9423)' in content
            assert 'dependencies/remove-auto-sizer-types' in content  # Verify non-ticket entries are preserved 