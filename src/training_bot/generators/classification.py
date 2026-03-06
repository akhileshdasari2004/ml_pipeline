from typing import List
from .base import BaseGenerator
from ..models.chunk import TextChunk
from ..models.example import TrainingExample
from ..models.task import TaskTemplate
from ..utils.helpers import generate_id
from ..utils.helpers import generate_id

class ClassificationGenerator(BaseGenerator):
    """Generates classification labels from text."""

    async def generate(self, chunk: TextChunk, task: TaskTemplate) -> List[TrainingExample]:
        prompt = f"Classify the following text into categories: {task.ai_params.get('categories', 'None')}\n\nText: {chunk.text}"
        response = await self.client.generate(prompt=prompt, **task.ai_params)
        
        return [TrainingExample(
            id=generate_id(f"{chunk.chunk_id}_clf"),
            document_id=chunk.document_id,
            chunk_id=chunk.chunk_id,
            input_text=chunk.text,
            output_text=response,
            metadata={"type": "classification"}
        )]
