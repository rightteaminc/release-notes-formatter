"""
Release Notes Parser Module

This module provides functionality to parse and process release notes from markdown files.
"""

from .models import ReleaseNoteEntry, EntryType
from .parser import ReleaseNoteParser

__all__ = ['ReleaseNoteEntry', 'EntryType', 'ReleaseNoteParser'] 