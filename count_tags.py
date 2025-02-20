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
    response = requests.get(github_api_url, headers=headers, params={"per_page": 100, "page": page})

    if response.status_code != 200:
        print(f"Error fetching tags: {response.json()}")
        return []

    tags = response.json()
    print(f"--- Found {len(tags)} tags for: {repo}")

    return tags

def count_tags_created_last_n_days(tags, days: int):
    """Counts the number of tags created within the last N days."""
    count = 0
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff_date = now - datetime.timedelta(days=days)

    print(f"--- Finding tags created in the last {days} days")

    for tag in tags:
        tag_name = tag["name"]
        tag_url = tag["commit"]["url"]

        commit_response = requests.get(tag_url, headers=headers)

        if commit_response.status_code != 200:
            print(f"Error fetching commit details for tag {tag_name}: {commit_response.json()}")
            continue

        commit_data = commit_response.json()
        commit_date = commit_data["commit"]["committer"]["date"]  # Example: "2024-02-12T14:30:00Z"
        commit_datetime = datetime.datetime.strptime(commit_date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)

        if commit_datetime >= cutoff_date:
            count += 1

    print(f"--- Found {count} tags in the last {days} days")

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

        tags = get_tags(organization, repo)

        if not tags:
            print(f"No tags found for {repo}, skipping...")
            results.append({"repo": repo, "last_30_days": 0, "last_90_days": 0})
            continue

        last_30_days = count_tags_created_last_n_days(tags, 30)
        last_90_days = count_tags_created_last_n_days(tags, 90)

        results.append({ "repo": repo, "last_30_days": last_30_days, "last_90_days": last_90_days })

    print("\n===== ============ =====\n")
    print(f"Results: {results}")
