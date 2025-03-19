from typing import Any

from .base import BaseIngestor


class AuthorsIngestor(BaseIngestor):
    """Ingestor for OpenAlex authors data."""

    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest authors data into the database."""
        # Authors table
        self._insert_dataframe("openalex.authors", data.get("authors", []))

        # Authors IDs table
        self._insert_dataframe("openalex.authors_ids", data.get("authors_ids", []))

        # Authors counts by year
        self._insert_dataframe(
            "openalex.authors_counts_by_year", data.get("authors_counts_by_year", [])
        )
