from enum import Enum

class TaskType(str, Enum):
    QA = "qa"
    SUMMARIZATION = "summarization"
    CLASSIFICATION = "classification"
    INSTRUCTION = "instruction"

class SourceType(str, Enum):
    WEB = "web"
    PDF = "pdf"
    MARKDOWN = "markdown"
    CSV = "csv"
    DOCX = "docx"

class ExportFormat(str, Enum):
    JSON = "json"
    JSONL = "jsonl"
    CSV = "csv"
    PARQUET = "parquet"

class QualityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
