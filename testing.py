import asyncio
import json
from typing import Any

import duckdb
import httpx
import polars as pl
from rich import print


async def get_from_autocomplete(
    search_str: str,
    client: httpx.AsyncClient,
    entity_type: str | None = None,
    autocomplete: bool = False,
) -> tuple[int, pl.DataFrame]:
    """
    use the OA autocomplete endpoint to get suggestions for a search string.
    """

    if entity_type not in [
        "works",
        "authors",
        "sources",
        "institutions",
        "concepts",
        "publishers",
        "funders",
    ]:
        entity_type = None

    url = "https://api.openalex.org"
    if not autocomplete and not entity_type:
        return 0, pl.DataFrame()

    if autocomplete:
        url += "/autocomplete"
        url += f"/{entity_type}?q={search_str}" if entity_type else f"?q={search_str}"
    else:
        url += f"/{entity_type}?search={search_str}"

    print(url)
    response: httpx.Response = await client.get(url)
    data: dict[str, dict | list[dict]] = response.json()
    count: int = data.get("meta", {}).get("count") or 0
    results = data.get("results", [])

    results: pl.DataFrame = pl.from_dicts(results) if results else pl.DataFrame()
    return count, results


def create_duckdb_connection(
    db_path: str = "openalex_data.duckdb",
) -> duckdb.DuckDBPyConnection:
    """Create and return a DuckDB connection."""
    return duckdb.connect(db_path)


def setup_duckdb_schema(conn: duckdb.DuckDBPyConnection) -> None:
    """Create tables in DuckDB based on OpenAlex schema."""

    # Create the schema
    conn.execute("CREATE SCHEMA IF NOT EXISTS openalex")

    # Authors tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.authors (
            id TEXT PRIMARY KEY,
            orcid TEXT,
            display_name TEXT,
            display_name_alternatives JSON,
            works_count INTEGER,
            cited_by_count INTEGER,
            last_known_institution TEXT,
            works_api_url TEXT,
            updated_date TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.authors_counts_by_year (
            author_id TEXT,
            year INTEGER,
            works_count INTEGER,
            cited_by_count INTEGER,
            oa_works_count INTEGER,
            PRIMARY KEY (author_id, year)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.authors_ids (
            author_id TEXT PRIMARY KEY,
            openalex TEXT,
            orcid TEXT,
            scopus TEXT,
            twitter TEXT,
            wikipedia TEXT,
            mag BIGINT
        )
    """)

    # Topics table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.topics (
            id TEXT PRIMARY KEY,
            display_name TEXT,
            subfield_id TEXT,
            subfield_display_name TEXT,
            field_id TEXT,
            field_display_name TEXT,
            domain_id TEXT,
            domain_display_name TEXT,
            description TEXT,
            keywords TEXT,
            works_api_url TEXT,
            wikipedia_id TEXT,
            works_count INTEGER,
            cited_by_count INTEGER,
            updated_date TIMESTAMP
        )
    """)

    # Concepts tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.concepts (
            id TEXT PRIMARY KEY,
            wikidata TEXT,
            display_name TEXT,
            level INTEGER,
            description TEXT,
            works_count INTEGER,
            cited_by_count INTEGER,
            image_url TEXT,
            image_thumbnail_url TEXT,
            works_api_url TEXT,
            updated_date TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.concepts_ancestors (
            concept_id TEXT,
            ancestor_id TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.concepts_counts_by_year (
            concept_id TEXT,
            year INTEGER,
            works_count INTEGER,
            cited_by_count INTEGER,
            oa_works_count INTEGER,
            PRIMARY KEY (concept_id, year)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.concepts_ids (
            concept_id TEXT PRIMARY KEY,
            openalex TEXT,
            wikidata TEXT,
            wikipedia TEXT,
            umls_aui JSON,
            umls_cui JSON,
            mag BIGINT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.concepts_related_concepts (
            concept_id TEXT,
            related_concept_id TEXT,
            score REAL
        )
    """)

    # Institutions tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.institutions (
            id TEXT PRIMARY KEY,
            ror TEXT,
            display_name TEXT,
            country_code TEXT,
            type TEXT,
            homepage_url TEXT,
            image_url TEXT,
            image_thumbnail_url TEXT,
            display_name_acronyms JSON,
            display_name_alternatives JSON,
            works_count INTEGER,
            cited_by_count INTEGER,
            works_api_url TEXT,
            updated_date TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.institutions_associated_institutions (
            institution_id TEXT,
            associated_institution_id TEXT,
            relationship TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.institutions_counts_by_year (
            institution_id TEXT,
            year INTEGER,
            works_count INTEGER,
            cited_by_count INTEGER,
            oa_works_count INTEGER,
            PRIMARY KEY (institution_id, year)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.institutions_geo (
            institution_id TEXT PRIMARY KEY,
            city TEXT,
            geonames_city_id TEXT,
            region TEXT,
            country_code TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.institutions_ids (
            institution_id TEXT PRIMARY KEY,
            openalex TEXT,
            ror TEXT,
            grid TEXT,
            wikipedia TEXT,
            wikidata TEXT,
            mag BIGINT
        )
    """)

    # Publishers tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.publishers (
            id TEXT PRIMARY KEY,
            display_name TEXT,
            alternate_titles JSON,
            country_codes JSON,
            hierarchy_level INTEGER,
            parent_publisher TEXT,
            works_count INTEGER,
            cited_by_count INTEGER,
            sources_api_url TEXT,
            updated_date TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.publishers_counts_by_year (
            publisher_id TEXT,
            year INTEGER,
            works_count INTEGER,
            cited_by_count INTEGER,
            oa_works_count INTEGER,
            PRIMARY KEY (publisher_id, year)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.publishers_ids (
            publisher_id TEXT,
            openalex TEXT,
            ror TEXT,
            wikidata TEXT
        )
    """)

    # Sources tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.sources (
            id TEXT PRIMARY KEY,
            issn_l TEXT,
            issn JSON,
            display_name TEXT,
            publisher TEXT,
            works_count INTEGER,
            cited_by_count INTEGER,
            is_oa BOOLEAN,
            is_in_doaj BOOLEAN,
            homepage_url TEXT,
            works_api_url TEXT,
            updated_date TIMESTAMP
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.sources_counts_by_year (
            source_id TEXT,
            year INTEGER,
            works_count INTEGER,
            cited_by_count INTEGER,
            oa_works_count INTEGER,
            PRIMARY KEY (source_id, year)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.sources_ids (
            source_id TEXT,
            openalex TEXT,
            issn_l TEXT,
            issn JSON,
            mag BIGINT,
            wikidata TEXT,
            fatcat TEXT
        )
    """)

    # Works tables
    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works (
            id TEXT PRIMARY KEY,
            doi TEXT,
            title TEXT,
            display_name TEXT,
            publication_year INTEGER,
            publication_date TEXT,
            type TEXT,
            cited_by_count INTEGER,
            is_retracted BOOLEAN,
            is_paratext BOOLEAN,
            cited_by_api_url TEXT,
            abstract TEXT,
            language TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_primary_locations (
            work_id TEXT,
            source_id TEXT,
            landing_page_url TEXT,
            pdf_url TEXT,
            is_oa BOOLEAN,
            version TEXT,
            license TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_locations (
            work_id TEXT,
            source_id TEXT,
            landing_page_url TEXT,
            pdf_url TEXT,
            is_oa BOOLEAN,
            version TEXT,
            license TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_best_oa_locations (
            work_id TEXT,
            source_id TEXT,
            landing_page_url TEXT,
            pdf_url TEXT,
            is_oa BOOLEAN,
            version TEXT,
            license TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_authorships (
            work_id TEXT,
            author_position TEXT,
            author_id TEXT,
            institution_id TEXT,
            raw_affiliation_string TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_biblio (
            work_id TEXT PRIMARY KEY,
            volume TEXT,
            issue TEXT,
            first_page TEXT,
            last_page TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_topics (
            work_id TEXT,
            topic_id TEXT,
            score REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_concepts (
            work_id TEXT,
            concept_id TEXT,
            score REAL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_ids (
            work_id TEXT PRIMARY KEY,
            openalex TEXT,
            doi TEXT,
            mag BIGINT,
            pmid TEXT,
            pmcid TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_mesh (
            work_id TEXT,
            descriptor_ui TEXT,
            descriptor_name TEXT,
            qualifier_ui TEXT,
            qualifier_name TEXT,
            is_major_topic BOOLEAN
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_open_access (
            work_id TEXT PRIMARY KEY,
            is_oa BOOLEAN,
            oa_status TEXT,
            oa_url TEXT,
            any_repository_has_fulltext BOOLEAN
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_referenced_works (
            work_id TEXT,
            referenced_work_id TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS openalex.works_related_works (
            work_id TEXT,
            related_work_id TEXT
        )
    """)

    # Indexes to improve query performance
    conn.execute(
        "CREATE INDEX IF NOT EXISTS concepts_ancestors_concept_id_idx ON openalex.concepts_ancestors(concept_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS concepts_related_concepts_concept_id_idx ON openalex.concepts_related_concepts(concept_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS concepts_related_concepts_related_concept_id_idx ON openalex.concepts_related_concepts(related_concept_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS works_authorships_work_id_idx ON openalex.works_authorships(work_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS works_concepts_work_id_idx ON openalex.works_concepts(work_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS works_primary_locations_work_id_idx ON openalex.works_primary_locations(work_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS works_locations_work_id_idx ON openalex.works_locations(work_id)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS works_best_oa_locations_work_id_idx ON openalex.works_best_oa_locations(work_id)"
    )


class OpenAlexParser:
    """Class to parse and flatten OpenAlex API data for database ingestion."""

    @staticmethod
    def invert_abstract(inv_index: dict | None):
        """Invert OpenAlex abstract index.

        Parameters
        ----------
        inv_index : dict
            Inverted index of the abstract.

        Returns
        -------
        str
            Inverted abstract.
        """
        if inv_index is None:
            return None
        try:
            l_inv_new = {}
            for w, pos in inv_index.items():
                if not pos:
                    continue
                l_inv_new[w] = pos
            l_inv = [(w, p) for w, pos in l_inv_new.items() for p in pos if pos]
        except TypeError:
            print(l_inv_new)

            input("Press Enter to continue...")
            return None
        return " ".join(map(lambda x: x[0], sorted(l_inv, key=lambda x: x[1])))

    @staticmethod
    def parse_authors(data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
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

    @staticmethod
    def parse_concepts(data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse concepts data from API response."""
        results = {
            "concepts": [],
            "concepts_ids": [],
            "concepts_ancestors": [],
            "concepts_counts_by_year": [],
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

            # Ancestors
            for ancestor in concept.get("ancestors") or []:
                if ancestor_id := ancestor.get("id"):
                    results["concepts_ancestors"].append(
                        {"concept_id": concept_id, "ancestor_id": ancestor_id}
                    )

            # Counts by year
            for count in concept.get("counts_by_year") or []:
                count_data = {
                    "concept_id": concept_id,
                    "year": count.get("year"),
                    "works_count": count.get("works_count"),
                    "cited_by_count": count.get("cited_by_count"),
                    "oa_works_count": count.get("oa_works_count"),
                }
                results["concepts_counts_by_year"].append(count_data)

            # Related concepts
            for related in concept.get("related_concepts") or []:
                if related_id := related.get("id"):
                    results["concepts_related_concepts"].append(
                        {
                            "concept_id": concept_id,
                            "related_concept_id": related_id,
                            "score": related.get("score"),
                        }
                    )

        return results

    @staticmethod
    def parse_works(data: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        """Parse works data from API response."""
        results = {
            "works": [],
            "works_authorships": [],
            "works_concepts": [],
            "works_ids": [],
            "works_open_access": [],
        }

        for work in data:
            work_id = work.get("id")
            if not work_id:
                continue

            # Main work data
            abstract = OpenAlexParser.invert_abstract(
                work.get("abstract_inverted_index")
            )
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

        return results


class OpenAlexIngestor:
    """Class to ingest flattened OpenAlex data into DuckDB."""

    def __init__(self, db_conn: duckdb.DuckDBPyConnection):
        self.conn = db_conn

    def ingest_authors(self, authors_data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest authors data into database."""
        # Authors table
        if authors_data["authors"]:
            authors_df = pl.DataFrame(authors_data["authors"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.authors
                SELECT * FROM authors_df
            """)

        # Authors IDs table
        if authors_data["authors_ids"]:
            authors_ids_df = pl.DataFrame(authors_data["authors_ids"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.authors_ids
                SELECT * FROM authors_ids_df
            """)

        # Authors counts by year
        if authors_data["authors_counts_by_year"]:
            counts_df = pl.DataFrame(authors_data["authors_counts_by_year"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.authors_counts_by_year
                SELECT * FROM counts_df
            """)

    def ingest_concepts(self, concepts_data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest concepts data into database."""
        # Concepts table
        if concepts_data["concepts"]:
            concepts_df = pl.DataFrame(concepts_data["concepts"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.concepts
                SELECT * FROM concepts_df
            """)

        # Concepts IDs table
        if concepts_data["concepts_ids"]:
            concepts_ids_df = pl.DataFrame(concepts_data["concepts_ids"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.concepts_ids
                SELECT * FROM concepts_ids_df
            """)

        # Concepts ancestors
        if concepts_data["concepts_ancestors"]:
            ancestors_df = pl.DataFrame(concepts_data["concepts_ancestors"])
            self.conn.execute("""
                INSERT INTO openalex.concepts_ancestors
                SELECT * FROM ancestors_df
            """)

        # Concepts counts by year
        if concepts_data["concepts_counts_by_year"]:
            counts_df = pl.DataFrame(concepts_data["concepts_counts_by_year"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.concepts_counts_by_year
                SELECT * FROM counts_df
            """)

        # Concepts related concepts
        if concepts_data["concepts_related_concepts"]:
            related_df = pl.DataFrame(concepts_data["concepts_related_concepts"])
            self.conn.execute("""
                INSERT INTO openalex.concepts_related_concepts
                SELECT * FROM related_df
            """)

    def ingest_works(self, works_data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest works data into database."""
        # Works table
        if works_data["works"]:
            works_df = pl.DataFrame(works_data["works"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.works
                SELECT * FROM works_df
            """)

        # Works authorships
        if works_data["works_authorships"]:
            authorships_df = pl.DataFrame(works_data["works_authorships"])
            self.conn.execute("""
                INSERT INTO openalex.works_authorships
                SELECT * FROM authorships_df
            """)

        # Works concepts
        if works_data["works_concepts"]:
            concepts_df = pl.DataFrame(works_data["works_concepts"])
            self.conn.execute("""
                INSERT INTO openalex.works_concepts
                SELECT * FROM concepts_df
            """)

        # Works IDs
        if works_data["works_ids"]:
            ids_df = pl.DataFrame(works_data["works_ids"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.works_ids
                SELECT * FROM ids_df
            """)

        # Works open access
        if works_data["works_open_access"]:
            oa_df = pl.DataFrame(works_data["works_open_access"])
            self.conn.execute("""
                INSERT OR REPLACE INTO openalex.works_open_access
                SELECT * FROM oa_df
            """)


async def retrieve_and_ingest(
    search_str: str,
    entity_type: str,
    client: httpx.AsyncClient,
    db_conn: duckdb.DuckDBPyConnection,
) -> tuple[int, list[dict]]:
    """Retrieve data from OpenAlex API, parse it and ingest into database."""
    count, data_df = await get_from_autocomplete(
        search_str, client, entity_type, autocomplete=False
    )

    if count == 0 or data_df.is_empty():
        return 0, []

    # Convert polars dataframe to list of dictionaries
    data_dicts = data_df.to_dicts()

    # Parse based on entity type
    parser = OpenAlexParser()
    ingestor = OpenAlexIngestor(db_conn)

    if entity_type == "authors":
        parsed_data = parser.parse_authors(data_dicts)
        ingestor.ingest_authors(parsed_data)
    elif entity_type == "concepts":
        parsed_data = parser.parse_concepts(data_dicts)
        ingestor.ingest_concepts(parsed_data)
    elif entity_type == "works":
        parsed_data = parser.parse_works(data_dicts)
        ingestor.ingest_works(parsed_data)
    else:
        # Handle other entity types if needed
        return count, data_dicts

    return count, data_dicts


async def main():
    """Example usage of the functions."""
    client = httpx.AsyncClient()
    db_conn = create_duckdb_connection()

    # Initialize database schema if needed
    setup_duckdb_schema(db_conn)

    # Example queries
    await retrieve_and_ingest("gardeniers", "authors", client, db_conn)
    await retrieve_and_ingest("porous silicon", "works", client, db_conn)

    # Example query to check the data
    authors_result = db_conn.execute("""
        SELECT a.display_name, a.works_count, a.cited_by_count
        FROM openalex.authors a
        WHERE a.display_name LIKE '%Gardeniers%'
    """).fetchall()

    print("Authors found:")
    for author in authors_result:
        print(f"Name: {author[0]}, Works: {author[1]}, Citations: {author[2]}")

    # Close connections
    await client.aclose()
    db_conn.close()


if __name__ == "__main__":
    asyncio.run(main())
