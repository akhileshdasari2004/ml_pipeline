from typing import Dict
from .base import BaseExporter
from .json_exporter import JSONExporter
from .csv_exporter import CSVExporter
from .parquet_exporter import ParquetExporter
from ..models.dataset import Dataset
from ..config.constants import ExportFormat

class ExportManager:
    """Manages data export to different formats."""

    def __init__(self):
        self.exporters: Dict[ExportFormat, BaseExporter] = {
            ExportFormat.JSON: JSONExporter(),
            ExportFormat.CSV: CSVExporter(),
            ExportFormat.PARQUET: ParquetExporter(),
        }

    async def export(self, dataset: Dataset, output_path: str, fmt: ExportFormat = ExportFormat.JSON) -> str:
        exporter = self.exporters.get(fmt)
        if not exporter:
            raise ValueError(f"No exporter for format: {fmt}")
        
        return await exporter.export(dataset, output_path)
