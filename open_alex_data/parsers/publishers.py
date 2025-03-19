import json
from typing import Any

from .base import BaseParser


class PublishersParser(BaseParser):
    """Parser for OpenAlex publishers data."""

    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse publishers data from API response."""
        results = {
            "publishers": [],
            "publishers_ids": [],
            "publishers_counts_by_year": [],
        }

        for publisher in data:
            publisher_id = publisher.get("id")
            if not publisher_id:
                continue

            # Main publisher data
            publisher_data = {
                "id": publisher_id,
                "display_name": publisher.get("display_name"),
                "alternate_titles": json.dumps(publisher.get("alternate_titles") or []),
                "country_codes": json.dumps(publisher.get("country_codes") or []),
                "hierarchy_level": publisher.get("hierarchy_level"),
                "parent_publisher": publisher.get("parent_publisher"),
                "works_count": publisher.get("works_count"),
                "cited_by_count": publisher.get("cited_by_count"),
                "sources_api_url": publisher.get("sources_api_url"),
                "updated_date": publisher.get("updated_date"),
            }
            results["publishers"].append(publisher_data)

            # Publisher IDs
            if ids := publisher.get("ids"):
                ids_data = {
                    "publisher_id": publisher_id,
                    "openalex": ids.get("openalex"),
                    "ror": ids.get("ror"),
                    "wikidata": ids.get("wikidata"),
                }
                results["publishers_ids"].append(ids_data)

            # Counts by year
            for count in publisher.get("counts_by_year") or []:
                count_data = {
                    "publisher_id": publisher_id,
                    "year": count.get("year"),
                    "works_count": count.get("works_count"),
                    "cited_by_count": count.get("cited_by_count"),
                    "oa_works_count": count.get("oa_works_count"),
                }
                results["publishers_counts_by_year"].append(count_data)

        return results
