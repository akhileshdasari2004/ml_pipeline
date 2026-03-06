from typing import List
from .base import BaseGenerator
from ..models.chunk import TextChunk
from ..models.example import TrainingExample
from ..models.task import TaskTemplate
from ..utils.helpers import generate_id
from ..utils.helpers import generate_id

class InstructionGenerator(BaseGenerator):
    """Generates instruction-following dataset examples."""

    async def generate(self, chunk: TextChunk, task: TaskTemplate) -> List[TrainingExample]:
        prompt = f"Create an instruction-response pair based on this text:\n\n{chunk.text}"
        response = await self.client.generate(prompt=prompt, **task.ai_params)
        
        return [TrainingExample(
            id=generate_id(f"{chunk.chunk_id}_inst"),
            document_id=chunk.document_id,
            chunk_id=chunk.chunk_id,
            input_text="Follow the instruction: " + chunk.text[:50], # Simplified
            output_text=response,
            metadata={"type": "instruction"}
        )]
