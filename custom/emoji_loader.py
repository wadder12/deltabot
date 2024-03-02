import yaml

def load_emojis(path='config/emojis.yaml'):
    """Load emojis from a YAML file."""
    try:
        with open(path, 'r') as file:
            emojis = yaml.safe_load(file).get('emojis', {})
    except FileNotFoundError:
        print(f"Error: The file {path} was not found.")
        emojis = {}
    return emojis
