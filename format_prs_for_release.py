import argparse
import subprocess
import json
from datetime import datetime

def parse_cli_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Process some dates and tags.')
    parser.add_argument('tag_name', type=str, help='Name of the tag.')
    parser.add_argument('--end_date', type=str, default=datetime.now().strftime('%Y-%m-%d'),
                        help='End date in DD-MM-YYYY format (optional, defaults to today\'s date).')

    return parser.parse_args()

def run_command(command):
  """Run shell command and return the output as JSON."""
  result = subprocess.run(command, text=True, capture_output=True, shell=True)

  if result.returncode != 0:
      raise Exception(f"Command failed: {result.stderr}")

  return json.loads(result.stdout)

def get_tag_date(owner, repo, tag_name):
  """Get the creation date of a git tag."""
  ref_data = run_command(f"gh api -X GET /repos/{owner}/{repo}/git/ref/tags/{tag_name}")
  object_type = ref_data['object']['type']
  object_id = ref_data['object']['sha']

  # Check if it's an annotated tag
  if object_type == "tag":
      # Fetch the tag object which includes the tagger's date
      tag_object = run_command(f"gh api -X GET /repos/{owner}/{repo}/git/tags/{object_id}")

      return tag_object['tagger']['date']
  elif object_type == "commit":
      # If it's a lightweight tag, fetch the commit to get the commit's date
      commit_object = run_command(f"gh api -X GET /repos/{owner}/{repo}/git/commits/{object_id}")

      return commit_object['committer']['date']

def fetch_prs(organization, repo, start_date, end_date):
    cmd = [
        "gh", "pr", "list", "--repo", f"{organization}/{repo}", "--state", "merged", "--base", "main",
        "--search", f"merged:{start_date}..{end_date}",
        "--json", "number,title,author,labels,mergedAt",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stdout:
        return json.loads(result.stdout)
    else:
        print("No data returned from GitHub CLI. Error:", result.stderr)
        return []

def format_pr_as_markdown(data_list):
  labels_of_interest = ["HOTFIX", "Bugfix", "Task", "Feature Flag", "Dependencies"]
  label_dict = {label: [] for label in labels_of_interest}
  markdown_output = ""

  for pr in data_list:
      for label in pr["labels"]:
          if label["name"] in labels_of_interest:
              label_dict[label["name"]].append(pr)

  for label, prs in label_dict.items():
      if prs:
          markdown_output += f"## {label}\n\n"

          for pr in prs:
              title = pr["title"]
              pr_number = pr["number"]
              author = pr["author"]["login"]
              markdown_output += f"- {title} (#{pr_number}) @{author}\n"

          markdown_output += "\n"

  return markdown_output

def write_to_file(draft, filename):
  with open(filename, 'w') as file:
      file.write(draft)

def main():
  owner = 'rightteaminc'
  repo = 'parallax'
  filename = 'input.md'

  args = parse_cli_args()

#   tag_date = get_tag_date(owner=owner, repo=repo, tag_name=args.tag_name)
  tag_date = '2024-05-30'
  merged_prs = fetch_prs(organization=owner, repo=repo, start_date=tag_date, end_date=args.end_date)
  markdown_output = format_pr_as_markdown(merged_prs)

  write_to_file(draft=markdown_output, filename=filename)

if __name__ == "__main__":
    main()
