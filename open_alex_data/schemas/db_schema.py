import duckdb


class DatabaseSchema:
    """Class to handle database schema creation and management."""

    @staticmethod
    def create_duckdb_connection(
        db_path: str = "openalex_data.duckdb",
    ) -> duckdb.DuckDBPyConnection:
        """Create and return a DuckDB connection.

        Parameters
        ----------
        db_path : str, optional
            Path to the DuckDB file, by default "openalex_data.duckdb"

        Returns
        -------
        duckdb.DuckDBPyConnection
            The DuckDB connection
        """
        return duckdb.connect(db_path)

    @staticmethod
    def setup_schema(conn: duckdb.DuckDBPyConnection) -> None:
        """Create OpenAlex schema in DuckDB.

        Parameters
        ----------
        conn : duckdb.DuckDBPyConnection
            The DuckDB connection
        """
        # Create schema
        conn.execute("CREATE SCHEMA IF NOT EXISTS openalex")

        # Create tables for each entity type
        DatabaseSchema._create_authors_tables(conn)
        DatabaseSchema._create_concepts_tables(conn)
        DatabaseSchema._create_works_tables(conn)
        DatabaseSchema._create_institutions_tables(conn)
        DatabaseSchema._create_topics_tables(conn)
        DatabaseSchema._create_publishers_tables(conn)
        DatabaseSchema._create_sources_tables(conn)

        # Create indexes
        DatabaseSchema._create_indexes(conn)

    @staticmethod
    def _create_authors_tables(conn: duckdb.DuckDBPyConnection) -> None:
        """Create tables for authors."""
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

    @staticmethod
    def _create_topics_tables(conn: duckdb.DuckDBPyConnection) -> None:
        """Create tables for topics."""
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

    @staticmethod
    def _create_concepts_tables(conn: duckdb.DuckDBPyConnection) -> None:
        """Create tables for concepts."""
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

    @staticmethod
    def _create_institutions_tables(conn: duckdb.DuckDBPyConnection) -> None:
        """Create tables for institutions."""
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

    @staticmethod
    def _create_publishers_tables(conn: duckdb.DuckDBPyConnection) -> None:
        """Create tables for publishers."""
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

    @staticmethod
    def _create_sources_tables(conn: duckdb.DuckDBPyConnection) -> None:
        """Create tables for sources."""
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

    @staticmethod
    def _create_works_tables(conn: duckdb.DuckDBPyConnection) -> None:
        """Create tables for works."""
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

    @staticmethod
    def _create_indexes(conn: duckdb.DuckDBPyConnection) -> None:
        """Create indexes to improve query performance."""
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
