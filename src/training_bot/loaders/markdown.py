from typing import List, Any
from ..models.document import SourceDocument
from pathlib import Path
from .base import BaseLoader
from ..config.constants import SourceType
from ..utils.errors import LoadError
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class MarkdownLoader(BaseLoader):
    """Loads text from Markdown files."""

    @property
    def source_type(self) -> SourceType:
        return SourceType.MARKDOWN

    async def load(self, file_path: str, **kwargs: Any) -> List[SourceDocument]:
        logger.info(f"Loading Markdown from {file_path}")
        path = Path(file_path)
        if not path.exists():
            raise LoadError(f"File not found: {file_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
                
                return [self._create_document(
                    content=content,
                    title=path.name,
                    id_prefix="md",
                    metadata={"file_path": str(path)}
                )]
        except Exception as e:
            logger.error(f"Failed to load Markdown {file_path}: {e}")
            raise LoadError(f"Markdown load failed: {e}")
