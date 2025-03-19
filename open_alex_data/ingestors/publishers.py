from typing import Any

from .base import BaseIngestor


class PublishersIngestor(BaseIngestor):
    """Ingestor for OpenAlex publishers data."""

    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest publishers data into the database."""
        # Publishers table
        self._insert_dataframe("openalex.publishers", data.get("publishers", []))

        # Publishers IDs table
        self._insert_dataframe(
            "openalex.publishers_ids", data.get("publishers_ids", [])
        )

        # Publishers counts by year
        self._insert_dataframe(
            "openalex.publishers_counts_by_year",
            data.get("publishers_counts_by_year", []),
        )
