from typing import Any

from .base import BaseParser


class WorksParser(BaseParser):
    """Parser for OpenAlex works data."""

    def parse(self, data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse works data from API response."""
        results = {
            "works": [],
            "works_authorships": [],
            "works_concepts": [],
            "works_ids": [],
            "works_open_access": [],
            "works_primary_locations": [],
            "works_locations": [],
            "works_best_oa_locations": [],
            "works_biblio": [],
            "works_topics": [],
            "works_mesh": [],
            "works_referenced_works": [],
            "works_related_works": [],
        }

        for work in data:
            work_id = work.get("id")
            if not work_id:
                continue

            # Main work data
            abstract = self.invert_abstract(work.get("abstract_inverted_index"))
            work_data = {
                "id": work_id,
                "doi": work.get("doi"),
                "title": work.get("title"),
                "display_name": work.get("display_name"),
                "publication_year": work.get("publication_year"),
                "publication_date": work.get("publication_date"),
                "type": work.get("type"),
                "cited_by_count": work.get("cited_by_count"),
                "is_retracted": work.get("is_retracted"),
                "is_paratext": work.get("is_paratext"),
                "cited_by_api_url": work.get("cited_by_api_url"),
                "abstract": abstract,
                "language": work.get("language"),
            }
            results["works"].append(work_data)

            # Authorships
            for authorship in work.get("authorships") or []:
                if not authorship.get("author"):
                    continue
                author_id = authorship.get("author", {}).get("id")
                if author_id:
                    institutions = authorship.get("institutions") or []
                    institution_ids = [i.get("id") for i in institutions if i.get("id")]

                    # If no institutions, still create record with null institution_id
                    if not institution_ids:
                        results["works_authorships"].append(
                            {
                                "work_id": work_id,
                                "author_position": authorship.get("author_position"),
                                "author_id": author_id,
                                "institution_id": None,
                                "raw_affiliation_string": authorship.get(
                                    "raw_affiliation_string"
                                ),
                            }
                        )
                    else:
                        # Create a record for each institution
                        for institution_id in institution_ids:
                            results["works_authorships"].append(
                                {
                                    "work_id": work_id,
                                    "author_position": authorship.get(
                                        "author_position"
                                    ),
                                    "author_id": author_id,
                                    "institution_id": institution_id,
                                    "raw_affiliation_string": authorship.get(
                                        "raw_affiliation_string"
                                    ),
                                }
                            )

            # Concepts
            for concept in work.get("concepts") or []:
                if concept_id := concept.get("id"):
                    results["works_concepts"].append(
                        {
                            "work_id": work_id,
                            "concept_id": concept_id,
                            "score": concept.get("score"),
                        }
                    )

            # IDs
            if ids := work.get("ids"):
                ids_data = {
                    "work_id": work_id,
                    "openalex": ids.get("openalex"),
                    "doi": ids.get("doi"),
                    "mag": ids.get("mag"),
                    "pmid": ids.get("pmid"),
                    "pmcid": ids.get("pmcid"),
                }
                results["works_ids"].append(ids_data)

            # Open access
            if oa := work.get("open_access"):
                oa_data = {
                    "work_id": work_id,
                    "is_oa": oa.get("is_oa"),
                    "oa_status": oa.get("oa_status"),
                    "oa_url": oa.get("oa_url"),
                    "any_repository_has_fulltext": oa.get(
                        "any_repository_has_fulltext"
                    ),
                }
                results["works_open_access"].append(oa_data)

            # Primary location
            if primary_location := work.get("primary_location"):
                if primary_location.get("source"):
                    if source_id := primary_location.get("source", {}).get("id"):
                        results["works_primary_locations"].append(
                            {
                                "work_id": work_id,
                                "source_id": source_id,
                                "landing_page_url": primary_location.get(
                                    "landing_page_url"
                                ),
                                "pdf_url": primary_location.get("pdf_url"),
                                "is_oa": primary_location.get("is_oa"),
                                "version": primary_location.get("version"),
                                "license": primary_location.get("license"),
                            }
                        )

            # Locations
            for location in work.get("locations") or []:
                if location.get("source"):
                    if source_id := location.get("source", {}).get("id"):
                        results["works_locations"].append(
                            {
                                "work_id": work_id,
                                "source_id": source_id,
                                "landing_page_url": location.get("landing_page_url"),
                                "pdf_url": location.get("pdf_url"),
                                "is_oa": location.get("is_oa"),
                                "version": location.get("version"),
                                "license": location.get("license"),
                            }
                        )

            # Best OA location
            if best_oa_location := work.get("best_oa_location"):
                if best_oa_location.get("source"):
                    if source_id := best_oa_location.get("source", {}).get("id"):
                        results["works_best_oa_locations"].append(
                            {
                                "work_id": work_id,
                                "source_id": source_id,
                                "landing_page_url": best_oa_location.get(
                                    "landing_page_url"
                                ),
                                "pdf_url": best_oa_location.get("pdf_url"),
                                "is_oa": best_oa_location.get("is_oa"),
                                "version": best_oa_location.get("version"),
                                "license": best_oa_location.get("license"),
                            }
                        )

            # Biblio
            if biblio := work.get("biblio"):
                results["works_biblio"].append(
                    {
                        "work_id": work_id,
                        "volume": biblio.get("volume"),
                        "issue": biblio.get("issue"),
                        "first_page": biblio.get("first_page"),
                        "last_page": biblio.get("last_page"),
                    }
                )

            # Topics
            for topic in work.get("topics") or []:
                if topic_id := topic.get("id"):
                    results["works_topics"].append(
                        {
                            "work_id": work_id,
                            "topic_id": topic_id,
                            "score": topic.get("score"),
                        }
                    )

            # Mesh
            for mesh in work.get("mesh") or []:
                results["works_mesh"].append(
                    {
                        "work_id": work_id,
                        "descriptor_ui": mesh.get("descriptor_ui"),
                        "descriptor_name": mesh.get("descriptor_name"),
                        "qualifier_ui": mesh.get("qualifier_ui"),
                        "qualifier_name": mesh.get("qualifier_name"),
                        "is_major_topic": mesh.get("is_major_topic"),
                    }
                )

            # Referenced works
            for ref_work_id in work.get("referenced_works") or []:
                if ref_work_id:
                    results["works_referenced_works"].append(
                        {
                            "work_id": work_id,
                            "referenced_work_id": ref_work_id,
                        }
                    )

            # Related works
            for related_work_id in work.get("related_works") or []:
                if related_work_id:
                    results["works_related_works"].append(
                        {
                            "work_id": work_id,
                            "related_work_id": related_work_id,
                        }
                    )

        return results
