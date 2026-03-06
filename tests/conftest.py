import pytest
from training_bot.models import SourceDocument, TextChunk, TrainingExample
from training_bot.config.constants import SourceType

@pytest.fixture
def sample_doc():
    return SourceDocument(
        id="test_doc",
        title="Test Doc",
        content="This is a test document with enough text to be chunked. " * 20,
        source_type=SourceType.MARKDOWN
    )

@pytest.fixture
def sample_chunk(sample_doc):
    return TextChunk(
        document_id=sample_doc.id,
        chunk_id="test_chunk",
        text=sample_doc.content[:100],
        index=0,
        start_idx=0,
        end_idx=100
    )
