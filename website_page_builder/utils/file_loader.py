# utils/file_loader.py
import os

def load_text_file(path: str) -> str:
    """Load a UTF-8 text file and return its contents as a string."""
    abs_path = os.path.abspath(path)
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()
