from typing import List
from .base import BaseGenerator
from ..models.chunk import TextChunk
from ..models.example import TrainingExample
from ..models.task import TaskTemplate
from ..utils.helpers import generate_id
from ..utils.helpers import generate_id

class SummarizationGenerator(BaseGenerator):
    """Generates summary pairs from text."""

    async def generate(self, chunk: TextChunk, task: TaskTemplate) -> List[TrainingExample]:
        prompt = f"Summarize the following text:\n\n{chunk.text}"
        response = await self.client.generate(prompt=prompt, **task.ai_params)
        
        return [TrainingExample(
            id=generate_id(f"{chunk.chunk_id}_sum"),
            document_id=chunk.document_id,
            chunk_id=chunk.chunk_id,
            input_text=chunk.text,
            output_text=response,
            metadata={"type": "summarization"}
        )]
