import subprocess
import json
from datetime import datetime
from collections import defaultdict

repository = "rightteaminc/parallax"
start_tag_name = "v15.5"
# next_tag_name = "v14.48.0"
title = ''
output_file_name = "commits.md"

tag_command = f"gh api repos/{repository}/git/refs/tags/{start_tag_name}"
output = subprocess.check_output(tag_command, shell=True).decode("utf-8")
tag_ref = json.loads(output)

if 'object' in tag_ref:
    tag_commit_sha = tag_ref['object']['sha']

    # Use the `gh api` command to list commits on the repository
    all_commits_command = f"gh api repos/{repository}/commits?per_page=1000"
    all_commits_output = subprocess.check_output(all_commits_command, shell=True).decode("utf-8")
    all_commits = json.loads(all_commits_output)

    # Filter commits from the tag to today
    today = datetime.now().isoformat()
    filtered_commits = [commit for commit in all_commits if commit['sha'] >= tag_commit_sha and commit['commit']['author']['date'] <= today]

    # Create a dictionary to group commits by label
    commits_by_label = defaultdict(list)

    # Fetch and store labels associated with each commit
    for commit in filtered_commits:
        labels_command = f"gh api repos/{repository}/commits/{commit['sha']}/pulls"
        labels_output = subprocess.check_output(labels_command, shell=True).decode("utf-8")
        labels_data = json.loads(labels_output)

        if labels_data:
            labels = [label['name'] for label in labels_data[0]['labels']]

            # Group commits by label
            for label in labels:
                commits_by_label[label].append(commit)

    with open(output_file_name, 'w') as f:
        f.write("# Title\n\n")

        # Iterate through each label and its associated commits
        for label, commits in commits_by_label.items():
            f.write(f"## {label}\n")

            for commit in commits:
                author = commit['author']['login']
                # Include only the first line of the commit message
                commit_message = commit['commit']['message'].split('\n', 1)[0]
                f.write(f"- {commit_message} @{author}\n")

            f.write("\n\n")
else:
    print(f"No commits found for tag: {start_tag_name}")
