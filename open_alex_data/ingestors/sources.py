from typing import Any

from .base import BaseIngestor


class SourcesIngestor(BaseIngestor):
    """Ingestor for OpenAlex sources data."""

    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest sources data into the database."""
        # Sources table
        self._insert_dataframe("openalex.sources", data.get("sources", []))

        # Sources IDs table
        self._insert_dataframe("openalex.sources_ids", data.get("sources_ids", []))

        # Sources counts by year
        self._insert_dataframe(
            "openalex.sources_counts_by_year", data.get("sources_counts_by_year", [])
        )
