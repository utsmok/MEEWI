from typing import Any

from .base import BaseParser


class TopicsParser(BaseParser):
    """Parser for OpenAlex topics data."""

    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse topics data from API response."""
        results = {"topics": []}

        for topic in data:
            topic_id = topic.get("id")
            if not topic_id:
                continue

            # Main topic data
            topic_data = {
                "id": topic_id,
                "display_name": topic.get("display_name"),
                "subfield_id": topic.get("subfield", {}).get("id"),
                "subfield_display_name": topic.get("subfield", {}).get("display_name"),
                "field_id": topic.get("field", {}).get("id"),
                "field_display_name": topic.get("field", {}).get("display_name"),
                "domain_id": topic.get("domain", {}).get("id"),
                "domain_display_name": topic.get("domain", {}).get("display_name"),
                "description": topic.get("description"),
                "keywords": "; ".join(topic.get("keywords") or []),
                "works_api_url": topic.get("works_api_url"),
                "wikipedia_id": topic.get("ids", {}).get("wikipedia"),
                "works_count": topic.get("works_count"),
                "cited_by_count": topic.get("cited_by_count"),
                "updated_date": topic.get("updated_date") or topic.get("updated"),
            }
            results["topics"].append(topic_data)

        return results
