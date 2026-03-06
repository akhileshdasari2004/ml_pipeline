import pandas as pd
from pathlib import Path
from .base import BaseExporter
from ..models.dataset import Dataset
from ..config.constants import ExportFormat

class CSVExporter(BaseExporter):
    """Exports dataset to CSV format."""

    @property
    def export_format(self) -> ExportFormat:
        return ExportFormat.CSV

    async def export(self, dataset: Dataset, output_path: str) -> str:
        data = [example.model_dump() for example in dataset.examples]
        df = pd.DataFrame(data)
        
        path = Path(output_path)
        if path.is_dir():
            path = path / f"dataset_{dataset.id}.csv"
        
        df.to_csv(path, index=False)
        return str(path)
