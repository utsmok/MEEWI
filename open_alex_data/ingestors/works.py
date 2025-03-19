from typing import Any

from .base import BaseIngestor


class WorksIngestor(BaseIngestor):
    """Ingestor for OpenAlex works data."""

    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest works data into the database."""
        # Works table
        self._insert_dataframe("openalex.works", data.get("works", []))

        # Works authorships
        self._insert_dataframe(
            "openalex.works_authorships", data.get("works_authorships", [])
        )

        # Works concepts
        self._insert_dataframe(
            "openalex.works_concepts", data.get("works_concepts", [])
        )

        # Works IDs
        self._insert_dataframe("openalex.works_ids", data.get("works_ids", []))

        # Works open access
        self._insert_dataframe(
            "openalex.works_open_access", data.get("works_open_access", [])
        )

        # Works primary locations
        self._insert_dataframe(
            "openalex.works_primary_locations", data.get("works_primary_locations", [])
        )

        # Works locations
        self._insert_dataframe(
            "openalex.works_locations", data.get("works_locations", [])
        )

        # Works best OA locations
        self._insert_dataframe(
            "openalex.works_best_oa_locations", data.get("works_best_oa_locations", [])
        )

        # Works biblio
        self._insert_dataframe("openalex.works_biblio", data.get("works_biblio", []))

        # Works topics
        self._insert_dataframe("openalex.works_topics", data.get("works_topics", []))

        # Works mesh
        self._insert_dataframe("openalex.works_mesh", data.get("works_mesh", []))

        # Works referenced works
        self._insert_dataframe(
            "openalex.works_referenced_works", data.get("works_referenced_works", [])
        )

        # Works related works
        self._insert_dataframe(
            "openalex.works_related_works", data.get("works_related_works", [])
        )
