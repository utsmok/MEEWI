from typing import Any

from .base import BaseIngestor


class FundersIngestor(BaseIngestor):
    """Ingestor for OpenAlex funders data."""

    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest funders data into the database."""
        # Funders table
        self._insert_dataframe("openalex.funders", data.get("funders", []))

        # Funders IDs table
        self._insert_dataframe("openalex.funders_ids", data.get("funders_ids", []))

        # Funders counts by year
        self._insert_dataframe(
            "openalex.funders_counts_by_year", data.get("funders_counts_by_year", [])
        )

        # Funders grants
        self._insert_dataframe(
            "openalex.funders_grants", data.get("funders_grants", [])
        )
