import os

from ai.core.loggers.file_logger import create_logger

logger = create_logger(
    app_name="sentiment_classification",
    log_filename=os.getenv("LOG_FILE_PATH", "/dev/fd/1"),
    err_filename=os.getenv("ERR_LOG_FILE_PATH", "/dev/fd/2"),
)

__all__ = ["logger"]
