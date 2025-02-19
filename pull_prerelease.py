import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

"""
Fetches draft releases from a given GitHub repository.

:param repo: Repository name with owner (e.g., 'rightteaminc/parallax')
:param token: GitHub Personal Access Token
:return: List of draft releases
"""
def get_draft_releases(repo, token):
    url = f"https://api.github.com/repos/{repo}/releases"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch releases:", response.text)
        return []

    releases = response.json()

    return [release for release in releases if release['draft']]

"""
Writes the content of a draft release to a file.

:param draft: The draft release data
:param filename: The file to write to
"""
def write_draft_to_file(draft, filename="input.md"):
    with open(filename, 'w') as file:
        file.write(draft['body'])

github_token = os.getenv('GITHUB_TOKEN')
repository = 'rightteaminc/parallax'

draft_releases = get_draft_releases(repository, github_token)

if draft_releases:
    write_draft_to_file(draft_releases[0])  # Write the first draft release to 'input.md'
    print("Draft release written to input.md")
else:
    print("No draft releases found")
