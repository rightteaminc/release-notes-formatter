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
from aggregate_ticket_ids import get_all_ticket_ids

load_dotenv()

organization = os.environ["AZURE_ORG"]
project = os.environ["AZURE_PROJECT"]
pat = os.environ["AZURE_PAT"]


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


def fetch_work_items(ticket_ids: List[int]) -> List[Dict]:
    """Fetch Azure details for all ticket IDs.
    
    Args:
        ticket_ids: List of ticket IDs to fetch.
        
    Returns:
        List of dictionaries containing complete entry details.
    """
    all_entries = []

    for ticket_id in ticket_ids:
        print(f"Fetching work item {ticket_id}...")
        azure_data = fetch_work_item(str(ticket_id))
        all_entries.append(azure_data)

    return all_entries


if __name__ == "__main__":
    output_filename = "tickets.yml"
    ticket_ids = get_all_ticket_ids()
    all_entries = fetch_work_items(ticket_ids)
    all_entries.sort(key=lambda x: int(x.get("id", 0)))
    
    with open(output_filename, "w", encoding="utf-8") as f:
        yaml.dump(all_entries, f, sort_keys=False, allow_unicode=True)

    print(f"{len(all_entries)} items written to {output_filename}")

