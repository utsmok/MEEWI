"""
Logging configuration for the application.

This module sets up loguru for system-wide logging and provides functions to
configure log levels and destinations.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

from loguru import logger

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)


def setup_logging(
    log_level: str = DEFAULT_LOG_LEVEL,
    log_file: str | Path | None = None,
    rotation: str = "10 MB",
    retention: str = "1 week",
) -> None:
    """
    Configure the application logging using loguru.

    Args:
        log_level: The log level for the application (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to the log file. If None, logs will only be sent to stderr.
        rotation: When to rotate the log file (e.g., "10 MB", "1 day")
        retention: How long to keep log files (e.g., "1 week", "1 month")
    """
    # Remove the default handler
    logger.remove()

    # Add stderr handler with appropriate log level
    logger.add(
        sys.stderr,
        level=log_level,
        format=DEFAULT_LOG_FORMAT,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    # Add file handler if log_file is specified
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            str(log_path),
            level=log_level,
            format=DEFAULT_LOG_FORMAT,
            rotation=rotation,
            retention=retention,
            compression="zip",
        )

    # Log the start of the application
    logger.info(
        "Logging initialized at {} - Log level: {}",
        datetime.now(timezone.utc).isoformat(),
        log_level,
    )


# Initialize with default settings
setup_logging()
