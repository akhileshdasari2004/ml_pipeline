from datetime import datetime
from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Job(BaseModel):
    """Tracks the progress of a pipeline job."""
    job_id: str
    status: JobStatus = JobStatus.PENDING
    progress: float = 0.0
    current_task: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    result: Optional[Any] = None

    def update_status(self, status: JobStatus, progress: float = 0.0, current_task: Optional[str] = None) -> None:
        self.status = status
        self.progress = progress
        self.current_task = current_task
        self.updated_at = datetime.now()
