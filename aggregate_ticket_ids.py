import os
from release_notes.parser import ReleaseNoteParser
from typing import List, Set

RAW_RELEASE_NOTES_DIR = 'raw_release_notes'

def extract_ticket_ids_from_file(filepath: str, parser: ReleaseNoteParser) -> Set[int]:
    """
    Extract ticket IDs from a single output.md file using the provided parser.
    """
    ticket_ids = set()
    entries = parser.parse_file(filepath)

    for entry in entries:
        if hasattr(entry, 'ticket_id') and entry.ticket_id is not None:
            ticket_ids.add(int(entry.ticket_id))
    
    return ticket_ids


def get_all_ticket_ids() -> List[int]:
    """
    Recursively find all output.md files in raw_release_notes/, extract ticket IDs, and return a deduplicated list.
    Returns:
        List[int]: Unique ticket IDs from all output.md files.
    """
    parser = ReleaseNoteParser()
    ticket_ids: Set[int] = set()

    for root, dirs, files in os.walk(RAW_RELEASE_NOTES_DIR):
        for file in files:
            if file == 'output.md':
                filepath = os.path.join(root, file)
                ticket_ids.update(extract_ticket_ids_from_file(filepath, parser))

    return sorted(ticket_ids) 