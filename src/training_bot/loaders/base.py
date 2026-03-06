import abc
from typing import Any, Dict, List, Optional
from ..models.document import SourceDocument
from ..config.constants import SourceType

class BaseLoader(abc.ABC):
    """Abstract base class for all document loaders."""

    @property
    @abc.abstractmethod
    def source_type(self) -> SourceType:
        """Type of source this loader handles."""
        pass

    @abc.abstractmethod
    async def load(self, source: str, **kwargs: Any) -> List[SourceDocument]:
        """Loads documents from a source."""
        pass

    def _create_document(self, content: str, title: str, id_prefix: str, **kwargs: Any) -> SourceDocument:
        """Helper to create a SourceDocument."""
        from ..utils.helpers import generate_id
        doc_id = f"{id_prefix}_{generate_id(content)[:8]}"
        return SourceDocument(
            id=doc_id,
            title=title,
            content=content,
            source_type=self.source_type,
            **kwargs
        )
