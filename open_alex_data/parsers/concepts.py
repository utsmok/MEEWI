import json
from typing import Any

from .base import BaseParser


class ConceptsParser(BaseParser):
    """Parser for OpenAlex concepts data."""

    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse concepts data from API response."""
        results = {
            "concepts": [],
            "concepts_ancestors": [],
            "concepts_counts_by_year": [],
            "concepts_ids": [],
            "concepts_related_concepts": [],
        }

        for concept in data:
            concept_id = concept.get("id")
            if not concept_id:
                continue

            # Main concept data
            concept_data = {
                "id": concept_id,
                "wikidata": concept.get("wikidata"),
                "display_name": concept.get("display_name"),
                "level": concept.get("level"),
                "description": concept.get("description"),
                "works_count": concept.get("works_count"),
                "cited_by_count": concept.get("cited_by_count"),
                "image_url": concept.get("image_url"),
                "image_thumbnail_url": concept.get("image_thumbnail_url"),
                "works_api_url": concept.get("works_api_url"),
                "updated_date": concept.get("updated_date"),
            }
            results["concepts"].append(concept_data)

            # Concept ancestors
            if ancestors := concept.get("ancestors"):
                for ancestor in ancestors:
                    if ancestor_id := ancestor.get("id"):
                        ancestor_data = {
                            "concept_id": concept_id,
                            "ancestor_id": ancestor_id,
                        }
                        results["concepts_ancestors"].append(ancestor_data)

            # Concept counts by year
            for count in concept.get("counts_by_year") or []:
                count_data = {
                    "concept_id": concept_id,
                    "year": count.get("year"),
                    "works_count": count.get("works_count"),
                    "cited_by_count": count.get("cited_by_count"),
                    "oa_works_count": count.get("oa_works_count"),
                }
                results["concepts_counts_by_year"].append(count_data)

            # Concept IDs
            if ids := concept.get("ids"):
                ids_data = {
                    "concept_id": concept_id,
                    "openalex": ids.get("openalex"),
                    "wikidata": ids.get("wikidata"),
                    "wikipedia": ids.get("wikipedia"),
                    "umls_aui": json.dumps(ids.get("umls_aui") or []),
                    "umls_cui": json.dumps(ids.get("umls_cui") or []),
                    "mag": ids.get("mag"),
                }
                results["concepts_ids"].append(ids_data)

            # Related concepts
            if related_concepts := concept.get("related_concepts"):
                for related in related_concepts:
                    if related_id := related.get("id"):
                        related_data = {
                            "concept_id": concept_id,
                            "related_concept_id": related_id,
                            "score": related.get("score"),
                        }
                        results["concepts_related_concepts"].append(related_data)

        return results
