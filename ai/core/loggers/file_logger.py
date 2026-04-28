import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

from loguru import logger
from ai.core.enums.log_level import LogLevel
from ai.core.constants.logging_constants import (
    DEFAULT_LOG_RETENTION_FILES,
    DEFAULT_LOG_ROTATION_SIZE,
)


def _is_regular_log_path(path: Union[str, Path]) -> bool:
    p = Path(path)

    # Treat these as streams, not files.
    if str(p) in {"/dev/stdout", "/dev/stderr"}:
        return False

    # If parent exists, ensure target is not a FIFO/device/etc.
    if p.exists():
        return p.is_file()

    return True


def _file_handler(
    filename: Union[str, Path],
    level: str,
    rotation: str,
    retention: int,
) -> Dict[str, Any]:
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    handler: Dict[str, Any] = {
        "sink": str(path),
        "serialize": True,
        "level": level,
        "enqueue": True,
    }

    if _is_regular_log_path(path):
        handler.update(
            {
                "rotation": rotation,
                "retention": retention,
            }
        )

    return handler


def create_logger(
    app_name: str,
    log_filename: Optional[Union[str, Path]],
    err_filename: Optional[Union[str, Path]] = None,
    log_level: LogLevel = LogLevel.DEBUG,
    rotation: str = DEFAULT_LOG_ROTATION_SIZE,
    retention: int = DEFAULT_LOG_RETENTION_FILES,
):
    handlers: list[Dict[str, Any]] = [
        {
            "sink": sys.stdout,
            "format": "{time} - {level} - {extra[app_name]} - {message}",
            "level": log_level.value,
            "enqueue": True,
        }
    ]

    if log_filename is not None:
        handlers.append(
            _file_handler(
                filename=log_filename,
                level=log_level.value,
                rotation=rotation,
                retention=retention,
            )
        )

    if err_filename is not None:
        handlers.append(
            _file_handler(
                filename=err_filename,
                level="ERROR",
                rotation=rotation,
                retention=retention,
            )
        )

    logger.configure(handlers=handlers)
    return logger.bind(app_name=app_name)

__all__ = ["create_logger"]