from typing import Any

from .base import BaseIngestor


class ConceptsIngestor(BaseIngestor):
    """Ingestor for OpenAlex concepts data."""

    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest concepts data into the database."""
        # Concepts table
        self._insert_dataframe("openalex.concepts", data.get("concepts", []))

        # Concepts ancestors table
        self._insert_dataframe(
            "openalex.concepts_ancestors", data.get("concepts_ancestors", [])
        )

        # Concepts counts by year
        self._insert_dataframe(
            "openalex.concepts_counts_by_year", data.get("concepts_counts_by_year", [])
        )

        # Concepts IDs table
        self._insert_dataframe("openalex.concepts_ids", data.get("concepts_ids", []))

        # Concepts related concepts
        self._insert_dataframe(
            "openalex.concepts_related_concepts",
            data.get("concepts_related_concepts", []),
        )
