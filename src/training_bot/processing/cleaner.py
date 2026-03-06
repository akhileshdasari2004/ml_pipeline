import re
import string
from typing import List

class TextCleaner:
    """Cleans raw text data."""

    def clean(self, text: str) -> str:
        """Main cleaning method."""
        if not text:
            return ""

        # Normalize whitespace
        text = self.normalize_whitespace(text)
        
        # Remove common noise
        text = self.remove_short_lines(text)
        
        return text.strip()

    def normalize_whitespace(self, text: str) -> str:
        """Replaces multiple spaces/newlines with single ones."""
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        return text

    def remove_short_lines(self, text: str, min_length: int = 10) -> str:
        """Removes lines that are likely navigation or noise."""
        lines = text.split("\n")
        cleaned_lines = [line for line in lines if len(line.strip()) >= min_length]
        return "\n".join(cleaned_lines)

    def remove_special_characters(self, text: str) -> str:
        """Removes non-printable characters."""
        printable = set(string.printable)
        return "".join(filter(lambda x: x in printable, text))
