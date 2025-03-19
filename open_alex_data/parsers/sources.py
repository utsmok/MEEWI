import json
from typing import Any

from .base import BaseParser


class SourcesParser(BaseParser):
    """Parser for OpenAlex sources data."""

    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse sources data from API response."""
        results = {"sources": [], "sources_ids": [], "sources_counts_by_year": []}

        for source in data:
            source_id = source.get("id")
            if not source_id:
                continue

            # Main source data
            source_data = {
                "id": source_id,
                "issn_l": source.get("issn_l"),
                "issn": json.dumps(source.get("issn") or []),
                "display_name": source.get("display_name"),
                "publisher": source.get("publisher"),
                "works_count": source.get("works_count"),
                "cited_by_count": source.get("cited_by_count"),
                "is_oa": source.get("is_oa"),
                "is_in_doaj": source.get("is_in_doaj"),
                "homepage_url": source.get("homepage_url"),
                "works_api_url": source.get("works_api_url"),
                "updated_date": source.get("updated_date"),
            }
            results["sources"].append(source_data)

            # Source IDs
            if ids := source.get("ids"):
                ids_data = {
                    "source_id": source_id,
                    "openalex": ids.get("openalex"),
                    "issn_l": ids.get("issn_l"),
                    "issn": json.dumps(ids.get("issn") or []),
                    "mag": ids.get("mag"),
                    "wikidata": ids.get("wikidata"),
                    "fatcat": ids.get("fatcat"),
                }
                results["sources_ids"].append(ids_data)

            # Counts by year
            for count in source.get("counts_by_year") or []:
                count_data = {
                    "source_id": source_id,
                    "year": count.get("year"),
                    "works_count": count.get("works_count"),
                    "cited_by_count": count.get("cited_by_count"),
                    "oa_works_count": count.get("oa_works_count"),
                }
                results["sources_counts_by_year"].append(count_data)

        return results
