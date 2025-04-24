"""
GitHub Release Notes Fetcher.

This module fetches draft releases from GitHub repositories and writes their content
to a markdown file for further processing.
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()


def get_draft_releases(repo: str, token: str) -> List[Dict]:
    """Fetches draft releases from a given GitHub repository.

    Args:
        repo: Repository name with owner (e.g., 'rightteaminc/parallax')
        token: GitHub Personal Access Token

    Returns:
        List of draft releases as dictionaries

    Raises:
        requests.RequestException: If the API request fails
    """
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch releases: {response.text}")
        return []

    releases = response.json()
    return [release for release in releases if release['draft']]


def write_draft_to_file(draft: Dict, filename: str = "input.md") -> None:
    """Writes the content of a draft release to a file.

    Args:
        draft: The draft release data dictionary
        filename: The file to write to (defaults to input.md)
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(draft['body'])


def fetch_and_save_latest_draft(repository: str, token: str, output_file: str = "input.md") -> bool:
    """Fetches the latest draft release and saves it to a file.

    Args:
        repository: Repository name with owner
        token: GitHub Personal Access Token
        output_file: Output file path (defaults to input.md)

    Returns:
        bool: True if a draft was found and saved, False otherwise
    """
    draft_releases = get_draft_releases(repository, token)
    
    if not draft_releases:
        print("No draft releases found")
        return False
        
    write_draft_to_file(draft_releases[0], output_file)
    print(f"Draft release written to {output_file}")
    return True


if __name__ == "__main__":
    github_token = os.getenv('GITHUB_TOKEN')
    repository = os.getenv('GITHUB_REPOSITORY', 'rightteaminc/parallax')
    
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable not set")
        exit(1)
        
    fetch_and_save_latest_draft(repository, github_token)
