"""
Base parser functionality to transform raw API data into standardized publication metadata.

This module provides classes and functions to parse and normalize metadata from
different sources into a consistent format.
"""

from typing import Any, Protocol

from models.schema import (
    PublicationMetadata,
)


class Parser(Protocol):
    """Protocol for metadata parsers."""

    def parse(self, raw_data: dict[str, Any]) -> PublicationMetadata | None:
        """
        Parse raw data into standardized publication metadata.

        Args:
            raw_data: The raw data from an API response

        Returns:
            A PublicationMetadata object or None if parsing failed
        """
        ...
