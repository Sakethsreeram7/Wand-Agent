# Basic logging setup and a decorator for logging function calls and exceptions
import logging
from functools import wraps

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
)

logger = logging.getLogger("WandAgentLogger")

def log_endpoint(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info(f"Calling endpoint: {func.__name__}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"Endpoint {func.__name__} succeeded.")
            return result
        except Exception as e:
            logger.exception(f"Exception in endpoint {func.__name__}: {e}")
            raise
    return wrapper
