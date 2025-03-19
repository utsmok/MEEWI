import asyncio
from typing import Any

import httpx
from api.client import OpenAlexClient
from ingestors import get_ingestor
from parsers import get_parser
from schemas.db_schema import DatabaseSchema

from models.enums import EntityType


class OpenAlexProcessor:
    """Main class for processing OpenAlex data."""

    def __init__(self, db_path: str = "openalex_data.duckdb", email: str = None):
        """Initialize the processor.

        Parameters
        ----------
        db_path : str, optional
            Path to the database file, by default "openalex_data.duckdb"
        email : str, optional
            Email to use for API requests (for polite pool), by default None
        """
        self.db_path = db_path
        self.client = OpenAlexClient(email)
        self.db_conn = None

    def connect_db(self) -> None:
        """Connect to the database."""
        self.db_conn = DatabaseSchema.create_duckdb_connection(self.db_path)

    def setup_schema(self) -> None:
        """Set up the database schema."""
        if not self.db_conn:
            self.connect_db()
        DatabaseSchema.setup_schema(self.db_conn)

    async def retrieve_and_ingest(
        self,
        search_str: str,
        entity_type: EntityType | str,
        http_client: httpx.AsyncClient,
    ) -> tuple[int, list[dict[str, Any]]]:
        """Retrieve data from OpenAlex API, parse and ingest it.

        Parameters
        ----------
        search_str : str
            Search string to query for
        entity_type : EntityType | str
            Type of entity to retrieve
        http_client : httpx.AsyncClient
            HTTP client to use for requests

        Returns
        -------
        Tuple[int, List[Dict[str, Any]]]
            Count of retrieved items and the raw data

        Raises
        ------
        ValueError
            If no parser or ingestor is available for the entity type
        """
        # Ensure database connection
        if not self.db_conn:
            self.connect_db()

        # Retrieve data from OpenAlex
        count, data_df = await self.client.get_from_autocomplete(
            search_str, http_client, entity_type, autocomplete=False
        )

        # If no results, return early
        if count == 0 or data_df.is_empty():
            return 0, []

        # Convert polars DataFrame to list of dictionaries
        data_dicts = data_df.to_dicts()

        # Parse data using the appropriate parser
        try:
            parser = get_parser(entity_type)
            parsed_data = parser.parse(data_dicts)
        except ValueError as e:
            print(f"Error getting parser: {e}")
            return count, data_dicts

        # Ingest data using the appropriate ingestor
        try:
            ingestor = get_ingestor(entity_type, self.db_conn)
            ingestor.ingest(parsed_data)
        except ValueError as e:
            print(f"Error getting ingestor: {e}")
            return count, data_dicts

        return count, data_dicts

    def close(self) -> None:
        """Close database connection."""
        if self.db_conn:
            self.db_conn.close()
            self.db_conn = None


async def main():
    """Example usage of the OpenAlex processor."""
    # Initialize processor
    processor = OpenAlexProcessor(email="your.email@example.com")
    processor.setup_schema()

    # Create HTTP client
    async with httpx.AsyncClient() as client:
        # Example queries
        await processor.retrieve_and_ingest("gardeniers", EntityType.AUTHORS, client)
        await processor.retrieve_and_ingest("porous silicon", EntityType.WORKS, client)
        await processor.retrieve_and_ingest("twente", EntityType.INSTITUTIONS, client)
        await processor.retrieve_and_ingest("optica", EntityType.PUBLISHERS, client)
        await processor.retrieve_and_ingest("twente", EntityType.SOURCES, client)

    # Close connections
    processor.close()


if __name__ == "__main__":
    asyncio.run(main())
