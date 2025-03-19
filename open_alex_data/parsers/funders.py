import json
from typing import Any

from .base import BaseParser


class FundersParser(BaseParser):
    """Parser for OpenAlex funders data."""

    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse funders data from API response."""
        results = {
            "funders": [],
            "funders_ids": [],
            "funders_counts_by_year": [],
            "funders_grants": [],
        }

        for funder in data:
            funder_id = funder.get("id")
            if not funder_id:
                continue

            # Main funder data
            funder_data = {
                "id": funder_id,
                "display_name": funder.get("display_name"),
                "country_code": funder.get("country_code"),
                "description": funder.get("description"),
                "homepage_url": funder.get("homepage_url"),
                "image_url": funder.get("image_url"),
                "image_thumbnail_url": funder.get("image_thumbnail_url"),
                "alternate_titles": json.dumps(funder.get("alternate_titles") or []),
                "works_count": funder.get("works_count"),
                "cited_by_count": funder.get("cited_by_count"),
                "grants_count": funder.get("grants_count"),
                "updated_date": funder.get("updated_date"),
            }
            results["funders"].append(funder_data)

            # Funder IDs
            if ids := funder.get("ids"):
                ids_data = {
                    "funder_id": funder_id,
                    "openalex": ids.get("openalex"),
                    "ror": ids.get("ror"),
                    "wikidata": ids.get("wikidata"),
                    "crossref": ids.get("crossref"),
                    "doi": ids.get("doi"),
                }
                results["funders_ids"].append(ids_data)

            # Counts by year
            for count in funder.get("counts_by_year") or []:
                count_data = {
                    "funder_id": funder_id,
                    "year": count.get("year"),
                    "works_count": count.get("works_count"),
                    "cited_by_count": count.get("cited_by_count"),
                    "oa_works_count": count.get("oa_works_count"),
                }
                results["funders_counts_by_year"].append(count_data)

            # Grants (if available)
            for grant in funder.get("grants") or []:
                if grant_id := grant.get("id"):
                    grant_data = {
                        "funder_id": funder_id,
                        "grant_id": grant_id,
                        "grant_number": grant.get("grant_number"),
                        "title": grant.get("title"),
                        "award_amount": grant.get("award_amount"),
                        "award_amount_currency": grant.get("award_amount_currency"),
                        "start_date": grant.get("start_date"),
                        "end_date": grant.get("end_date"),
                    }
                    results["funders_grants"].append(grant_data)

        return results
