import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
headers = {"Authorization": f"token {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}

def get_tags(organization: str, repo: str):
    """Fetches all tags for the repository."""
    print(f"--- Fetching tags for: {repo}")

    tags = []
    page = 1
    github_api_url = f"https://api.github.com/repos/{organization}/{repo}/tags"
    response = requests.get(github_api_url, headers=headers, params={"per_page": 50, "page": page})

    if response.status_code != 200:
        print(f"Error fetching tags: {response.json()}")

        return []

    tags = response.json()

    print(f"--- Found {len(tags)} tags for: {repo}")

    return tags

def count_tags_created_this_month(organization: str, repo: str):
    """Counts the number of tags created in the current month."""
    count = 0
    now = datetime.datetime.now(datetime.timezone.utc)
    current_year = now.year
    current_month = now.month

    tags = get_tags(organization, repo)

    print(f"--- Finding this month's tags for {repo}")

    for tag in tags:
        tag_name = tag["name"]
        tag_url = tag["commit"]["url"]

        commit_response = requests.get(tag_url, headers=headers)

        if commit_response.status_code != 200:
            print(f"Error fetching commit details for tag {tag_name}: {commit_response.json()}")
            continue

        commit_data = commit_response.json()
        commit_date = commit_data["commit"]["committer"]["date"]  # Example: "2024-02-12T14:30:00Z"
        commit_datetime = datetime.datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ")

        if commit_datetime.year == current_year and commit_datetime.month == current_month:
            count += 1

    print(f"--- Found {count} tags for {repo}")

    return count


if __name__ == "__main__":
  organization = 'rightteaminc'
  repos = [
      'parallax',
      'parallax-server',
  ]
  results = []

  for repo in repos:
    print(f"\nGetting Tags for: {repo}")

    tag_count = count_tags_created_this_month(organization, repo)
    results.append({ "repo": repo, "count": tag_count })

  print("\n===== ============ =====\n")
  print(f"Results: {results}")
