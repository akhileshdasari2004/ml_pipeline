import hashlib
import json
from pathlib import Path
from typing import Any, Union
from datetime import datetime

def generate_id(content: str) -> str:
    """Generates a stable SHA-256 hash for content."""
    return hashlib.sha256(content.encode()).hexdigest()

def ensure_dir(path: Union[str, Path]) -> Path:
    """Ensures a directory exists."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def format_timestamp(dt: datetime = None) -> str:
    """Formats timestamp for file names."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y%m%d_%H%M%S")

async def save_json(data: Any, path: Union[str, Path], indent: int = 4) -> None:
    """Saves data as JSON file."""
    import aiofiles
    async with aiofiles.open(path, 'w') as f:
        await f.write(json.dumps(data, indent=indent, default=str))

async def load_json(path: Union[str, Path]) -> Any:
    """Loads data from JSON file."""
    import aiofiles
    async with aiofiles.open(path, 'r') as f:
        content = await f.read()
        return json.loads(content)
