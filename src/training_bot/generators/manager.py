from typing import Dict, List
from .base import BaseGenerator
from .qa_generator import QAGenerator
from .summarization import SummarizationGenerator
from .classification import ClassificationGenerator
from .instruction import InstructionGenerator
from ..models.chunk import TextChunk
from ..models.example import TrainingExample
from ..models.task import TaskTemplate
from ..config.constants import TaskType
from .client import AIClient

class TaskManager:
    """Routes tasks to the appropriate generator."""

    def __init__(self, client: AIClient):
        self.client = client
        self.generators: Dict[TaskType, BaseGenerator] = {
            TaskType.QA: QAGenerator(client),
            TaskType.SUMMARIZATION: SummarizationGenerator(client),
            TaskType.CLASSIFICATION: ClassificationGenerator(client),
            TaskType.INSTRUCTION: InstructionGenerator(client),
        }

    async def run_task(self, chunk: TextChunk, task: TaskTemplate) -> List[TrainingExample]:
        generator = self.generators.get(task.task_type)
        if not generator:
            raise ValueError(f"No generator found for task type: {task.task_type}")
        
        return await generator.generate(chunk, task)
