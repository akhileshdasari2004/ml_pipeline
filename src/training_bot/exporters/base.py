import abc
from typing import Any, Union
from pathlib import Path
from ..models.dataset import Dataset
from ..config.constants import ExportFormat

class BaseExporter(abc.ABC):
    """Abstract base class for exporters."""

    @property
    @abc.abstractmethod
    def export_format(self) -> ExportFormat:
        pass

    @abc.abstractmethod
    async def export(self, dataset: Dataset, output_path: Union[str, Path]) -> str:
        pass
