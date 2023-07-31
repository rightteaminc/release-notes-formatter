import re

def replace_match(match, base_url):
    number = match.group(1)
    formatted_number = f'AB#{number}'
    link = f'[{formatted_number}]({base_url}{number})'
    
    return link

def build_release_item_text(markdown_content, base_url):
    pattern = r'(?<=- )AB[#-]?(\d+)\s*-?\s*'
    transformed_content = re.sub(pattern, lambda match: replace_match(match, base_url) + ' - ', markdown_content)
    
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

    transform_markdown(input_file_name, output_file_name, base_url)
