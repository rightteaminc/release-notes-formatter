import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# GitHub API token (optional, for higher rate limits)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Repository details
ORG = "rightteaminc"
REPO = "parallax"
# REPO = "parallax-server"
GITHUB_API_URL = f"https://api.github.com/repos/{ORG}/{REPO}/tags"

now = datetime.datetime.now(datetime.timezone.utc)
current_year = now.year
current_month = now.month
headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def get_tags():
    """Fetches all tags for the repository."""
    tags = []
    page = 1

    response = requests.get(GITHUB_API_URL, headers=headers, params={"per_page": 100, "page": page})

    if response.status_code != 200:
        print(f"Error fetching tags: {response.json()}")

        return []

    tags = response.json()

    return tags

def count_tags_created_this_month():
    """Counts the number of tags created in the current month."""
    tags = get_tags()
    count = 0

    for tag in tags:
        tag_name = tag["name"]
        tag_url = tag["commit"]["url"]  # Get commit URL for the tag

        commit_response = requests.get(tag_url, headers=headers)

        if commit_response.status_code != 200:
            print(f"Error fetching commit details for tag {tag_name}: {commit_response.json()}")
            continue

        commit_data = commit_response.json()
        commit_date = commit_data["commit"]["committer"]["date"]  # Example: "2024-02-12T14:30:00Z"
        commit_datetime = datetime.datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")

        if commit_datetime.year == current_year and commit_datetime.month == current_month:
            count += 1

    print(f"For: {ORG}/{REPO} in {current_year}-{current_month}")
    print(f"Number of tags: {count}")


count_tags_created_this_month()
