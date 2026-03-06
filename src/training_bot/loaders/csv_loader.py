import pandas as pd
from typing import List, Any
from ..models.document import SourceDocument
from pathlib import Path
from .base import BaseLoader
from ..config.constants import SourceType
from ..utils.errors import LoadError
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class CSVLoader(BaseLoader):
    """Loads tabular data from CSV files."""

    @property
    def source_type(self) -> SourceType:
        return SourceType.CSV

    async def load(self, file_path: str, **kwargs: Any) -> List[SourceDocument]:
        logger.info(f"Loading CSV from {file_path}")
        path = Path(file_path)
        try:
            df = pd.read_csv(path)
            content = df.to_string()
            return [self._create_document(
                content=content,
                title=path.name,
                id_prefix="csv",
                metadata={"file_path": str(path), "rows": len(df)}
            )]
        except Exception as e:
            logger.error(f"Failed to load CSV {file_path}: {e}")
            raise LoadError(f"CSV load failed: {e}")
