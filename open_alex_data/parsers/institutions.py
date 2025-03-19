import json
from typing import Any

from .base import BaseParser


class InstitutionsParser(BaseParser):
    """Parser for OpenAlex institutions data."""

    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse institutions data from API response."""
        results = {
            "institutions": [],
            "institutions_ids": [],
            "institutions_geo": [],
            "institutions_associated_institutions": [],
            "institutions_counts_by_year": [],
        }

        for institution in data:
            institution_id = institution.get("id")
            if not institution_id:
                continue

            # Main institution data
            institution_data = {
                "id": institution_id,
                "ror": institution.get("ror"),
                "display_name": institution.get("display_name"),
                "country_code": institution.get("country_code"),
                "type": institution.get("type"),
                "homepage_url": institution.get("homepage_url"),
                "image_url": institution.get("image_url"),
                "image_thumbnail_url": institution.get("image_thumbnail_url"),
                "display_name_acronyms": json.dumps(
                    institution.get("display_name_acronyms") or []
                ),
                "display_name_alternatives": json.dumps(
                    institution.get("display_name_alternatives") or []
                ),
                "works_count": institution.get("works_count"),
                "cited_by_count": institution.get("cited_by_count"),
                "works_api_url": institution.get("works_api_url"),
                "updated_date": institution.get("updated_date"),
            }
            results["institutions"].append(institution_data)

            # Institution IDs
            if ids := institution.get("ids"):
                ids_data = {
                    "institution_id": institution_id,
                    "openalex": ids.get("openalex"),
                    "ror": ids.get("ror"),
                    "grid": ids.get("grid"),
                    "wikipedia": ids.get("wikipedia"),
                    "wikidata": ids.get("wikidata"),
                    "mag": ids.get("mag"),
                }
                results["institutions_ids"].append(ids_data)

            # Institution geo
            if geo := institution.get("geo"):
                geo_data = {
                    "institution_id": institution_id,
                    "city": geo.get("city"),
                    "geonames_city_id": geo.get("geonames_city_id"),
                    "region": geo.get("region"),
                    "country_code": geo.get("country_code"),
                    "country": geo.get("country"),
                    "latitude": geo.get("latitude"),
                    "longitude": geo.get("longitude"),
                }
                results["institutions_geo"].append(geo_data)

            # Associated institutions - handle both "associated_institutions" and the API typo "associated_insitutions"
            associated = (
                institution.get("associated_institutions")
                or institution.get("associated_insitutions")
                or []
            )
            for assoc in associated:
                if assoc_id := assoc.get("id"):
                    assoc_data = {
                        "institution_id": institution_id,
                        "associated_institution_id": assoc_id,
                        "relationship": assoc.get("relationship"),
                    }
                    results["institutions_associated_institutions"].append(assoc_data)

            # Counts by year
            for count in institution.get("counts_by_year") or []:
                count_data = {
                    "institution_id": institution_id,
                    "year": count.get("year"),
                    "works_count": count.get("works_count"),
                    "cited_by_count": count.get("cited_by_count"),
                    "oa_works_count": count.get("oa_works_count"),
                }
                results["institutions_counts_by_year"].append(count_data)

        return results
