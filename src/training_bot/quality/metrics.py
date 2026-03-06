from typing import List
from ..models.example import TrainingExample

def coherence_score(example: TrainingExample) -> float:
    """Calculates coherence score (placeholder)."""
    return 1.0

def relevance_score(example: TrainingExample, chunk_text: str) -> float:
    """Calculates relevance score (placeholder)."""
    return 1.0

def calculate_overall_metrics(examples: List[TrainingExample]) -> dict:
    """Aggregates metrics across examples."""
    return {
        "avg_score": sum(e.quality_score for e in examples) / len(examples) if examples else 0,
        "count": len(examples)
    }
