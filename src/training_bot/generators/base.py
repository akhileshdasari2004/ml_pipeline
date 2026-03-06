from typing import Any, List
from ..models.chunk import TextChunk
from ..models.example import TrainingExample
from ..models.task import TaskTemplate
from .client import AIClient
from ..utils.helpers import generate_id
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class BaseGenerator:
    """Base class for all task generators."""

    def __init__(self, client: AIClient):
        self.client = client

    async def generate(self, chunk: TextChunk, task: TaskTemplate) -> List[TrainingExample]:
        """Generates training examples from a chunk."""
        raise NotImplementedError
