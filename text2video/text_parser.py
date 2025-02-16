import re
import os

def parse_text_file(input_path: str):
    """
    Read the file, return a list of lines/sentences,
    and extract title from filename (part after last '/' and before '.').
    """
    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read().strip()

    # Split by sentences using regex
    lines = re.split(r'[.!?]+', raw_text)
    lines = [ln.strip() for ln in lines if ln.strip()]

    # Extract title from filename using os.path
    title = os.path.splitext(os.path.basename(input_path))[0]

    return lines, title