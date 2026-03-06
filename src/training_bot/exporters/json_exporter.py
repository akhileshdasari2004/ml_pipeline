import json
from pathlib import Path
from .base import BaseExporter
from ..models.dataset import Dataset
from ..config.constants import ExportFormat
from ..utils.helpers import save_json

class JSONExporter(BaseExporter):
    """Exports dataset to JSON format."""

    @property
    def export_format(self) -> ExportFormat:
        return ExportFormat.JSON

    async def export(self, dataset: Dataset, output_path: str) -> str:
        data = [example.model_dump() for example in dataset.examples]
        path = Path(output_path)
        if path.is_dir():
            path = path / f"dataset_{dataset.id}.json"
        
        await save_json(data, path)
        return str(path)
