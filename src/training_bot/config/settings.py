import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Base Paths
ROOT_DIR = Path(__file__).parent.parent.parent.parent
DATA_DIR = Path(os.getenv("DATA_DIR", ROOT_DIR / "data"))
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", DATA_DIR / "outputs"))
LOGS_DIR = ROOT_DIR / "logs"

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Processing Settings
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 1000))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 200))

# AI Settings
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-4-turbo")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
MAX_RETRIES = 3
RETRY_MIN_SECONDS = 1
RETRY_MAX_SECONDS = 10

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
