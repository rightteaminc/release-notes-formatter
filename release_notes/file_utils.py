import yaml

def load_repositories_from_yaml(yaml_path: str = "repos.yml") -> list:
    """Load repositories from a YAML file."""
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
   
    return data.get('repositories', []) 