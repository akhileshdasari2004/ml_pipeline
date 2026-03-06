import json
from typing import List
from .base import BaseGenerator
from ..models.chunk import TextChunk
from ..models.example import TrainingExample
from ..models.task import TaskTemplate
from ..utils.helpers import generate_id

class QAGenerator(BaseGenerator):
    """Generates Question-Answer pairs from text."""

    async def generate(self, chunk: TextChunk, task: TaskTemplate) -> List[TrainingExample]:
        prompt = task.prompt_template.replace("{{text}}", chunk.text)
        if chunk.prev_context:
            prompt = prompt.replace("{{prev_context}}", chunk.prev_context)
        if chunk.next_context:
            prompt = prompt.replace("{{next_context}}", chunk.next_context)

        response = await self.client.generate(
            prompt=prompt,
            system_prompt=task.system_prompt or "You are an expert at generating high-quality QA pairs for ML training.",
            **task.ai_params
        )

        try:
            # Expecting JSON format from AI
            data = json.loads(response)
            examples = []
            for item in data:
                examples.append(TrainingExample(
                    id=generate_id(f"{chunk.chunk_id}_{item['question']}"),
                    document_id=chunk.document_id,
                    chunk_id=chunk.chunk_id,
                    input_text=item['question'],
                    output_text=item['answer'],
                    metadata={"model": task.ai_params.get("model", "default"), "type": "qa"}
                ))
            return examples
        except Exception as e:
            # Fallback if AI doesn't return JSON
            return [TrainingExample(
                id=generate_id(f"{chunk.chunk_id}_raw"),
                document_id=chunk.document_id,
                chunk_id=chunk.chunk_id,
                input_text=chunk.text[:100],
                output_text=response,
                metadata={"error": str(e), "raw_response": response}
            )]
