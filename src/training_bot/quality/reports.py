import json
from typing import List
from ..models.dataset import Dataset
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class ReportGenerator:
    """Generates quality audit reports for datasets."""

    def generate_report(self, dataset: Dataset) -> str:
        report = {
            "dataset_name": dataset.name,
            "total_examples": len(dataset.examples),
            "stats": dataset.stats,
            "examples_sample": [e.model_dump() for e in dataset.examples[:5]]
        }
        return json.dumps(report, indent=4)
