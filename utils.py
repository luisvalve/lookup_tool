
import time
import functools
from core.logger import logger


def retry(max_attempts=2, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Attempt {attempt} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            logger.error(f"All {max_attempts} attempts failed for function {func.__name__}")
            return None
        return wrapper
    return decorator


def sleep(seconds):
    logger.debug(f"Sleeping for {seconds} seconds...")
    time.sleep(seconds)
