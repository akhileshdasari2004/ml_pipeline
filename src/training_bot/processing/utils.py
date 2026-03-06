from typing import List
import re

def count_tokens(text: str) -> int:
    """Approximate token count (simple word-based for now)."""
    # In a real app, use tiktoken or similar
    return len(re.findall(r'\w+', text))

def normalize_text(text: str) -> str:
    """Basic text normalization."""
    return text.lower().strip()

def detect_language(text: str) -> str:
    """Placeholder for language detection."""
    # Would use lingua-language-detector here
    return "en"
