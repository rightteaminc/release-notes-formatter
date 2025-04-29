"""
Data models for release notes parsing.

This module contains the data structures used to represent release note entries.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class EntryType(Enum):
    """Enum representing different types of release note entries."""
    AZURE_TICKET = "azure_ticket"
    DEPENDENCY_UPDATE = "dependency_update"
    CUSTOM = "custom"
    WORK_ITEM = "work_item"

@dataclass
class ReleaseNoteEntry:
    """Data class representing a single release note entry."""
    raw_text: str
    entry_type: EntryType
    section: Optional[str] = None  # Section the entry belongs to (e.g., "🏷 Enhancements")
    ticket_id: Optional[int] = None
    title: Optional[str] = None
    author: Optional[str] = None
    pr_number: Optional[str] = None  # Changed from int to str to preserve leading zeros and match test expectations 