"""
GitHub Release Notes Fetcher.

This module fetches draft releases from GitHub repositories and writes their content
to a markdown file for further processing.
"""

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict, Optional
import yaml
from release_notes.file_utils import load_repositories_from_yaml

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
        print(f"[ERROR] Failed to fetch releases: {response.text}")

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


def fetch_and_save_latest_draft(repo_obj: dict, token: str, output_dir: str) -> bool:
    """Fetches the latest draft release (or most recent release if no draft) and saves it to a file in the given directory."""
    repository = repo_obj['repo']
    repo_name = repo_obj['name']
    output_file = os.path.join(output_dir, repo_name, "input.md")
    draft_releases = get_draft_releases(repository, token)
    
    if draft_releases:
        write_draft_to_file(draft_releases[0], output_file)
        print(f"[INFO] Draft release written to {output_file}")
        
        return True
    
    # Fallback: fetch all releases and use the most recent (non-draft)
    url = f"https://api.github.com/repos/{repository}/releases"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"[ERROR] Failed to fetch releases: {response.text}")
        return False
    
    releases = response.json()
    non_draft_releases = [release for release in releases if not release['draft']]
    
    if not non_draft_releases:
        print("[WARN] No releases found")
        return False
    
    write_draft_to_file(non_draft_releases[0], output_file)
    
    print(f"[INFO] No draft found. Most recent release written to {output_file}")
    
    return True


def load_repositories_from_yaml(yaml_path: str = "repos.yml") -> list:
    """Load repositories from a YAML file."""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    return data.get('repositories', [])


if __name__ == "__main__":
    github_token = os.getenv('GITHUB_TOKEN')
    root_dir = "raw_release_notes"
    
    if not github_token:
        print("[ERROR] GITHUB_TOKEN environment variable not set")
        exit(1)

    repositories = load_repositories_from_yaml()
    summary = []

    for repo in repositories:
        repo_dir = os.path.join(root_dir, repo['name'])
        input_path = os.path.join(repo_dir, "input.md")

        if not os.path.exists(repo_dir):
            os.makedirs(repo_dir)

        print(f"[INFO] Fetching release notes for {repo['name']}...")
        
        try:
            result = fetch_and_save_latest_draft(repo, github_token, root_dir)
            status = "Success" if result else "No release found"
        except Exception as e:
            print(f"[ERROR] Failed to fetch for {repo['name']}: {e}")
            status = f"Error: {e}"
            
        summary.append({
            'name': repo['name'],
            'input_path': input_path,
            'status': status
        })

    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    print("\nSummary of input.md generation:")
    print(f"{'Repository':<20} {'Input File':<50} {'Status'}")
    print("-" * 90)

    for entry in summary:
        print(f"{entry['name']:<20} {entry['input_path']:<50} {entry['status']}")

    print("\n")