from typing import List, Optional, Any
from .models import SourceDocument, TextChunk, TrainingExample, Dataset, Job, JobStatus, TaskTemplate
from .loaders.unified import UnifiedLoader
from .processing.pipeline import ProcessingPipeline
from .generators.client import AIClient
from .generators.manager import TaskManager
from .quality.evaluator import QualityEvaluator
from .exporters.manager import ExportManager
from .utils.logging import setup_logging
from .utils.cost_monitor import CostMonitor
from .utils.helpers import generate_id
from .config.constants import SourceType, ExportFormat, TaskType

logger = setup_logging(__name__)

class TrainingDataBot:
    """Main orchestrator for the training data pipeline."""

    def __init__(self, api_key: Optional[str] = None):
        self.cost_monitor = CostMonitor()
        self.ai_client = AIClient(cost_monitor=self.cost_monitor)
        
        self.loader = UnifiedLoader()
        self.processor = ProcessingPipeline()
        self.task_manager = TaskManager(self.ai_client)
        self.quality_evaluator = QualityEvaluator()
        self.export_manager = ExportManager()
        
        self._documents: List[SourceDocument] = []
        self._chunks: List[TextChunk] = []
        self._examples: List[TrainingExample] = []
        self._jobs: List[Job] = []

    async def load_documents(self, source: str, source_type: Optional[SourceType] = None) -> List[SourceDocument]:
        """Loads and stores documents."""
        logger.info(f"Loading documents from {source}")
        docs = await self.loader.load(source, source_type)
        self._documents.extend(docs)
        return docs

    async def process_documents(self) -> List[TextChunk]:
        """Runs the cleaning and chunking pipeline."""
        logger.info("Processing documents into chunks")
        chunks = self.processor.process(self._documents)
        self._chunks.extend(chunks)
        return chunks

    async def generate_training_data(self, task: TaskTemplate) -> List[TrainingExample]:
        """Generates examples for all loaded chunks."""
        logger.info(f"Generating training data for task: {task.task_type}")
        new_examples = []
        for chunk in self._chunks:
            examples = await self.task_manager.run_task(chunk, task)
            new_examples.extend(examples)
        
        self._examples.extend(new_examples)
        return new_examples

    async def evaluate_quality(self) -> List[TrainingExample]:
        """Evaluates quality of generated examples."""
        logger.info("Evaluating quality of generated examples")
        self._examples = self.quality_evaluator.evaluate(self._examples)
        return self._examples

    async def export(self, name: str, fmt: ExportFormat = ExportFormat.JSON, output_dir: str = "data/outputs") -> str:
        """Exports the dataset."""
        logger.info(f"Exporting dataset {name} to {fmt}")
        dataset = Dataset(
            id=generate_id(name),
            name=name,
            examples=self._examples
        )
        dataset.update_stats()
        
        return await self.export_manager.export(dataset, output_dir, fmt)

    def get_stats(self) -> dict:
        """Returns pipeline statistics."""
        return {
            "documents": len(self._documents),
            "chunks": len(self._chunks),
            "examples": len(self._examples),
            **self.cost_monitor.get_summary()
        }
