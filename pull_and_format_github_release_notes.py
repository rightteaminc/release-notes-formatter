import subprocess
import re
import os
import yaml
from release_notes.file_utils import load_repositories_from_yaml

def pull_current_draft_release():
    # this should pull the current release draft from GitHub
    command = 'gh release view $(gh release list --limit 1 | awk \'NR==1{print $1}\')'
    output_filename = 'input.md'
    output = subprocess.run(command, shell=True, capture_output=True, text=True).stdout

    with open(output_filename, 'a') as file:
        file.write(output)

def format_ticket_number(match, base_url):
    number = match.group(1)
    formatted_number = f'AB#{number}'
    link = f'[{formatted_number}]({base_url}{number})'
    
    return link

def format_ticket_number_list(match, base_url):
    return format_ticket_number(match, base_url)

def build_release_item_text(markdown_content, base_url):
    pattern = r'(?<=- )AB[#-]?(\d+)\s*-?\s*'
    transformed_content = re.sub(pattern, lambda match: format_ticket_number_list(match, base_url) + ' - ', markdown_content)
    
    return transformed_content

def transform_markdown(input_file, output_file, base_url, repo_obj=None):
    """Transform markdown from input_file to output_file using base_url. Optionally, use repo_obj for future extensibility."""
    with open(input_file, 'r') as f:
        markdown_content = f.read()
    
    final_content = build_release_item_text(markdown_content, base_url)

    with open(output_file, 'w') as f:
        f.write(final_content)

if __name__ == "__main__":
    root_dir = "raw_release_notes"
    base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'
    repositories = load_repositories_from_yaml()
    summary = []

    for repo in repositories:
        repo_dir = os.path.join(root_dir, repo['name'])
        input_file_name = os.path.join(repo_dir, 'input.md')
        output_file_name = os.path.join(repo_dir, 'output.md')

        if not os.path.exists(input_file_name):
            print(f"[WARN] Input file not found for {repo['name']}: {input_file_name}")
            
            summary.append({
                'name': repo['name'],
                'output_path': output_file_name,
                'status': 'Skipped (input.md not found)'
            })
            
            continue

        print(f"[INFO] Formatting release notes for {repo['name']}...")

        try:
            transform_markdown(input_file_name, output_file_name, base_url, repo_obj=repo)
            status = 'Success'
        except Exception as e:
            print(f"[ERROR] Failed to format for {repo['name']}: {e}")
            status = f'Error: {e}'

        summary.append({
            'name': repo['name'],
            'output_path': output_file_name,
            'status': status
        })

    print("\nSummary of output.md generation:")
    print(f"{'Repository':<20} {'Output File':<50} {'Status'}")
    print("-" * 90)
    for entry in summary:
        print(f"{entry['name']:<20} {entry['output_path']:<50} {entry['status']}")
