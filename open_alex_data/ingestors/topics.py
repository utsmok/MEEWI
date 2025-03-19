from typing import Any

from .base import BaseIngestor


class TopicsIngestor(BaseIngestor):
    """Ingestor for OpenAlex topics data."""

    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest topics data into the database."""
        # Topics table
        self._insert_dataframe("openalex.topics", data.get("topics", []))
