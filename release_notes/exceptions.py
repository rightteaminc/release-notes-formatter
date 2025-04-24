"""
Custom exceptions for the release notes parser.

This module contains custom exceptions used throughout the release notes parser.
"""

class ReleaseNoteParseError(Exception):
    """Base exception for release note parsing errors."""
    pass

class InvalidEntryFormatError(ReleaseNoteParseError):
    """Exception raised when an entry cannot be parsed due to invalid format."""
    pass 