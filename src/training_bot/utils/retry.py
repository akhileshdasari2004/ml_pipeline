import time
import asyncio
import functools
import random
from typing import Any, Callable, TypeVar
from .logging import setup_logging
from ..config.settings import MAX_RETRIES, RETRY_MIN_SECONDS, RETRY_MAX_SECONDS

logger = setup_logging(__name__)

T = TypeVar("T")

def retry_with_backoff(
    retries: int = MAX_RETRIES,
    min_delay: int = RETRY_MIN_SECONDS,
    max_delay: int = RETRY_MAX_SECONDS,
    exceptions: tuple = (Exception,),
) -> Callable:
    """Decorator for exponential backoff retry logic."""
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception = None
            for attempt in range(retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == retries:
                        break
                    
                    delay = min(min_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    await asyncio.sleep(delay)
            
            logger.error(f"All {retries + 1} attempts failed for {func.__name__}.")
            raise last_exception
        return wrapper
    return decorator
