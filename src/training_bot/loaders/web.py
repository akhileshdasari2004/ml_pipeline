from typing import List, Any
from ..models.document import SourceDocument
import httpx
from bs4 import BeautifulSoup
from .base import BaseLoader
from ..config.constants import SourceType
from ..utils.errors import LoadError
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class WebLoader(BaseLoader):
    """Loads content from web URLs."""

    @property
    def source_type(self) -> SourceType:
        return SourceType.WEB

    async def load(self, url: str, **kwargs: Any) -> List[SourceDocument]:
        logger.info(f"Loading web content from {url}")
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                title = soup.title.string if soup.title else url
                content = soup.get_text(separator="\n", strip=True)
                
                return [self._create_document(
                    content=content,
                    title=title,
                    id_prefix="web",
                    source_url=url,
                    metadata={"url": url}
                )]
        except Exception as e:
            logger.error(f"Failed to load web content from {url}: {e}")
            raise LoadError(f"Web load failed: {e}")
