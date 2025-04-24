"""
Parser for release notes.

This module contains the parser implementation for processing release note entries.
"""

import re
from typing import List, Optional, Match, Callable, Dict, Tuple
from .models import ReleaseNoteEntry, EntryType
from .exceptions import InvalidEntryFormatError

class ReleaseNoteParser:
    """Parser for release note entries from markdown files."""
    
    def __init__(self):
        # Simple pattern that matches everything between @ and the next space
        self._author_pattern = r"@(\S+)"
        
        self._patterns: Dict[str, Tuple[str, Callable[[str, Match], ReleaseNoteEntry]]] = {
            'azure_ticket': (
                fr"- \[AB#(\d+)\]\(.*?\) - (.*?) {self._author_pattern} \(#(\d+)\)",
                self._create_azure_entry
            ),
            'non_azure': (
                fr"- (.*?) {self._author_pattern} \(#(\d+)\)",
                self._create_non_azure_entry
            )
        }
        self._section_pattern = re.compile(r"^##\s+(.+)$")
    
    def parse_line(self, line: str) -> Optional[ReleaseNoteEntry]:
        """Parse a single line from a release note file.
        
        Args:
            line: A single line from the release notes file.
            
        Returns:
            ReleaseNoteEntry if the line matches any known pattern, None otherwise.
            
        Raises:
            InvalidEntryFormatError: If the line partially matches a pattern but is malformed.
        """
        # Check for partial matches that might indicate malformed entries
        if line.startswith('- ['):
            if not re.match(r"- \[AB#\d+\]", line):
                raise InvalidEntryFormatError(f"Malformed Azure ticket entry: {line}")
        
        # Try each pattern in order (most specific to least specific)
        for pattern_name in ['azure_ticket', 'non_azure']:
            pattern, handler = self._patterns[pattern_name]
            if match := re.match(pattern, line):
                try:
                    return handler(line, match)
                except (IndexError, ValueError) as e:
                    raise InvalidEntryFormatError(f"Malformed entry: {line}") from e
        
        # If line starts with "- " but didn't match any pattern, it's probably malformed
        if line.startswith('- '):
            raise InvalidEntryFormatError(f"Unrecognized entry format: {line}")
        
        return None
    
    def _extract_author(self, match: Match, author_group_start: int = 1) -> str:
        """Extract author from a match group."""
        author = match.group(author_group_start)
        # Special case for renovate[bot]
        if author == '[renovate[bot]](https://github.com/apps/renovate)':
            return 'renovate[bot]'
        # Handle markdown-style links: @[name](link)
        if author.startswith('[') and ')' in author:
            # Extract just the name from [name](link)
            author = author[1:author.index(']')]
        return author
    
    def _create_azure_entry(self, raw_text: str, match: Match) -> ReleaseNoteEntry:
        """Create an Azure ticket entry from regex match."""
        try:
            ticket_id = int(match.group(1))
            title = match.group(2)
            author = self._extract_author(match, author_group_start=3)
            pr_number = match.group(4)
        except (ValueError, IndexError) as e:
            raise InvalidEntryFormatError(f"Invalid ticket or PR number in: {raw_text}") from e
            
        return ReleaseNoteEntry(
            raw_text=raw_text,
            entry_type=EntryType.AZURE_TICKET,
            ticket_id=ticket_id,
            title=title,
            author=author,
            pr_number=pr_number
        )
    
    def _create_non_azure_entry(self, raw_text: str, match: Match) -> ReleaseNoteEntry:
        """Create a non-Azure entry (custom or dependency) from regex match."""
        try:
            title = match.group(1)
            author = self._extract_author(match, author_group_start=2)
            pr_number = match.group(3)
        except (ValueError, IndexError) as e:
            raise InvalidEntryFormatError(f"Invalid PR number in: {raw_text}") from e
            
        # Mark as dependency if it's in the Dependencies section or has dependency-related keywords
        is_dependency = any(keyword in title.lower() for keyword in [
            'dependency', 'dependencies', 'update', 'upgrade'
        ])
            
        return ReleaseNoteEntry(
            raw_text=raw_text,
            entry_type=EntryType.DEPENDENCY_UPDATE if is_dependency else EntryType.CUSTOM,
            title=title,
            author=author,
            pr_number=pr_number
        )
    
    def parse_file(self, filepath: str) -> List[ReleaseNoteEntry]:
        """Parse an entire release note file.
        
        Args:
            filepath: Path to the release notes file.
            
        Returns:
            List of ReleaseNoteEntry objects for each valid line in the file.
        """
        entries = []
        current_section = None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                if not line:
                    continue
                    
                if section_match := self._section_pattern.match(line):
                    current_section = section_match.group(1)
                    continue
                
                try:
                    if entry := self.parse_line(line):
                        entry.section = current_section
                        
                        if current_section and '🧩 Dependencies' in current_section:
                            entry.entry_type = EntryType.DEPENDENCY_UPDATE
                        entries.append(entry)
                except InvalidEntryFormatError:
                    continue
                    
        return entries 