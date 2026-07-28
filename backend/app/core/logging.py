"""Structured JSON logging configuration."""

import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Configure structured logging format for ProjectIQ."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
