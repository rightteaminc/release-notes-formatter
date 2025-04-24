import subprocess
import re

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

def transform_markdown(input_file, output_file, base_url):
    with open(input_file, 'r') as f:
        markdown_content = f.read()
    
    final_content = build_release_item_text(markdown_content, base_url)

    with open(output_file, 'w') as f:
        f.write(final_content)

if __name__ == "__main__":
    input_file_name = 'input.md'
    output_file_name = 'output.md'
    base_url = 'https://dev.azure.com/parallax-app/Parallax%202023/_workitems/edit/'

    # pull_current_draft_release()
    transform_markdown(input_file_name, output_file_name, base_url)
