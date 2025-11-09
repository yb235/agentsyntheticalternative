"""Logging utilities."""

import sys
from loguru import logger
from typing import Optional


def setup_logging(level: str = "INFO", log_file: Optional[str] = None):
    """Setup logging configuration."""
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=level,
        colorize=True,
    )
    
    # Add file handler if specified
    if log_file:
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
            level=level,
            rotation="10 MB",
            retention="1 week",
        )
    
    return logger


def get_logger(name: Optional[str] = None):
    """Get a logger instance."""
    if name:
        return logger.bind(name=name)
    return logger
