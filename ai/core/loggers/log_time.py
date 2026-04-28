from time import time
from typing import List, Callable, Any
from loguru import logger as loguru_logger  # Import the instance, not a class


def log_time(trace_args: List[str] = [], logger: Any=None):
    # If no logger is provided, default to the global loguru logger
    actual_logger = logger if logger is not None else loguru_logger

    def log_time_decorator(func: Callable):
        def handler(*args, **kwargs):
            start = time()
            result = func(*args, **kwargs)
            duration = time() - start

            tracable_args = [f"{arg}:{kwargs[arg]}" for arg in kwargs.keys() if arg in trace_args]
            trace_args_str = ", ".join(tracable_args) if tracable_args else ""

            actual_logger.info(
                f"{func.__module__}:{func.__name__} takes {duration:.4f}s.\n"
                f"{trace_args_str}\n{'-' * 20}"
            )
            return result

        return handler

    return log_time_decorator