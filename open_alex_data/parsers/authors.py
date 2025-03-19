import json
from typing import Any

from .base import BaseParser


class AuthorsParser(BaseParser):
    """Parser for OpenAlex authors data."""

    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse authors data from API response."""
        results = {"authors": [], "authors_ids": [], "authors_counts_by_year": []}

        for author in data:
            author_id = author.get("id")
            if not author_id:
                continue

            # Main author data
            author_data = {
                "id": author_id,
                "orcid": author.get("orcid"),
                "display_name": author.get("display_name"),
                "display_name_alternatives": json.dumps(
                    author.get("display_name_alternatives") or []
                ),
                "works_count": author.get("works_count"),
                "cited_by_count": author.get("cited_by_count"),
                "last_known_institution": (
                    author.get("last_known_institution") or {}
                ).get("id"),
                "works_api_url": author.get("works_api_url"),
                "updated_date": author.get("updated_date"),
            }
            results["authors"].append(author_data)

            # Author IDs
            if ids := author.get("ids"):
                ids_data = {
                    "author_id": author_id,
                    "openalex": ids.get("openalex"),
                    "orcid": ids.get("orcid"),
                    "scopus": ids.get("scopus"),
                    "twitter": ids.get("twitter"),
                    "wikipedia": ids.get("wikipedia"),
                    "mag": ids.get("mag"),
                }
                results["authors_ids"].append(ids_data)

            # Counts by year
            for count in author.get("counts_by_year") or []:
                count_data = {
                    "author_id": author_id,
                    "year": count.get("year"),
                    "works_count": count.get("works_count"),
                    "cited_by_count": count.get("cited_by_count"),
                    "oa_works_count": count.get("oa_works_count"),
                }
                results["authors_counts_by_year"].append(count_data)

        return results
