from typing import Any

from .base import BaseIngestor


class InstitutionsIngestor(BaseIngestor):
    """Ingestor for OpenAlex institutions data."""

    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest institutions data into the database."""
        # Institutions table
        self._insert_dataframe("openalex.institutions", data.get("institutions", []))

        # Institutions IDs table
        self._insert_dataframe(
            "openalex.institutions_ids", data.get("institutions_ids", [])
        )

        # Institutions geo table
        self._insert_dataframe(
            "openalex.institutions_geo", data.get("institutions_geo", [])
        )

        # Institutions associated institutions
        self._insert_dataframe(
            "openalex.institutions_associated_institutions",
            data.get("institutions_associated_institutions", []),
        )

        # Institutions counts by year
        self._insert_dataframe(
            "openalex.institutions_counts_by_year",
            data.get("institutions_counts_by_year", []),
        )
