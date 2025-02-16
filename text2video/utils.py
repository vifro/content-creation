import re

def get_title_slug(title: str) -> str:
    """
    Convert title to a file-system friendly slug, e.g., 'My Great Title' -> 'my_great_title'.
    """
    slug = re.sub(r'[^a-zA-Z0-9]+', '_', title)
    return slug.lower()
