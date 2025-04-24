"""
Azure DevOps ticket fetcher.

This module extracts ticket IDs from markdown files and fetches their details from Azure DevOps.
It also processes non-Azure entries like dependencies and custom changes.
"""

import requests
import os
import re
import yaml
from dataclasses import asdict
from typing import Dict, List, Optional, Union
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from release_notes.parser import ReleaseNoteParser
from release_notes.models import EntryType, ReleaseNoteEntry

load_dotenv()

organization = os.environ["AZURE_ORG"]
project = os.environ["AZURE_PROJECT"]
pat = os.environ["AZURE_PAT"]


def parse_release_notes(filepath: str) -> List[ReleaseNoteEntry]:
    """Parse release notes and extract all entries with their metadata.
    
    Args:
        filepath: Path to the markdown file to parse.
        
    Returns:
        A list of ReleaseNoteEntry objects for all entry types.
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist.
    """
    parser = ReleaseNoteParser()
    return parser.parse_file(filepath)


def fetch_work_item(work_item_id: str) -> Dict:
    """Fetch details of a single work item from Azure DevOps.
    
    Args:
        work_item_id: The ID of the work item to fetch.
        
    Returns:
        A dictionary containing the work item's details.
        
    Raises:
        SystemExit: If the API request fails.
    """
    url = f"https://dev.azure.com/{organization}/_apis/wit/workitems/{work_item_id}?api-version=7.0"
    response = requests.get(url, auth=HTTPBasicAuth('', pat))

    if response.status_code != 200:
        print(f"Error fetching work item: {response.status_code}")
        print(response.text)
        exit(1)

    data = response.json()
    title = data['fields'].get('System.Title')
    raw_description = data['fields'].get('System.Description')
    soup = BeautifulSoup(raw_description or "", 'html.parser')
    clean_description = soup.get_text(separator="\n").strip()

    return {
        "id": work_item_id,
        "title": title,
        "description": clean_description
    }


def fetch_work_items(entries: List[ReleaseNoteEntry]) -> List[Dict]:
    """Process all entries and fetch Azure details where applicable.
    
    Args:
        entries: List of ReleaseNoteEntry objects of any type.
        
    Returns:
        List of dictionaries containing complete entry details.
    """
    all_entries = []

    for entry in entries:
        entry_dict = asdict(entry)
        entry_dict["entry_type"] = entry_dict["entry_type"].value  
        
        if entry.entry_type == EntryType.AZURE_TICKET and entry.ticket_id is not None:
            print(f"Fetching work item {entry.ticket_id}...")
            azure_data = fetch_work_item(str(entry.ticket_id))
            entry_dict.update({
                "azure_title": azure_data["title"],
                "azure_description": azure_data["description"]
            })
        
        all_entries.append(entry_dict)

    return all_entries


if __name__ == "__main__":
    output_filename = "tickets.yml"
    entries = parse_release_notes("output.md")
    all_entries = fetch_work_items(entries)
    all_entries.sort(key=lambda x: x.get("ticket_id", 0) or 0)
    
    with open(output_filename, "w", encoding="utf-8") as f:
        yaml.dump(all_entries, f, sort_keys=False, allow_unicode=True)

    print(f"{len(all_entries)} items written to {output_filename}")

