from typing import List
from ..models.example import TrainingExample

class QualityFilter:
    """Filters examples based on quality thresholds."""

    def __init__(self, min_score: float = 0.7):
        self.min_score = min_score

    def filter(self, examples: List[TrainingExample]) -> List[TrainingExample]:
        return [e for e in examples if e.quality_score >= self.min_score]

    def deduplicate(self, examples: List[TrainingExample]) -> List[TrainingExample]:
        """Simple deduplication based on input hash."""
        seen = set()
        unique = []
        for e in examples:
            if e.input_text not in seen:
                seen.add(e.input_text)
                unique.append(e)
        return unique
