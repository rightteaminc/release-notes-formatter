"""
Shared test fixtures for the release notes parser tests.
"""

import pytest
from pathlib import Path
from release_notes.parser import ReleaseNoteParser
from release_notes.models import ReleaseNoteEntry, EntryType

@pytest.fixture
def parser():
    """Provide a ReleaseNoteParser instance."""
    return ReleaseNoteParser()

@pytest.fixture
def sample_release_notes():
    """Path to the sample release notes markdown file."""
    return Path(__file__).parent / "fixtures" / "sample_release_notes.md"

@pytest.fixture
def sample_azure_ticket_entry():
    """Sample Azure ticket entry text."""
    return "- [AB#1234](https://dev.azure.com/org/project/_workitems/edit/1234) - Test ticket @user (#100)"

@pytest.fixture
def sample_dependency_entry():
    """Sample dependency update entry text."""
    return "- Update all non-major dependencies @renovate[bot] (#101)"

@pytest.fixture
def sample_custom_entry():
    """Sample custom entry text."""
    return "- custom/change @user (#102)" 