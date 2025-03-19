from abc import ABC, abstractmethod
from typing import Any

import duckdb
import polars as pl


class BaseIngestor(ABC):
    """Base class for ingesting parsed data into a database."""

    def __init__(self, conn: duckdb.DuckDBPyConnection):
        """Initialize the ingestor with a database connection.

        Parameters
        ----------
        conn : duckdb.DuckDBPyConnection
            The DuckDB connection to use for ingestion
        """
        self.conn = conn
        self._tables_with_constraints = None

    @abstractmethod
    def ingest(self, data: dict[str, list[dict[str, Any]]]) -> None:
        """Ingest parsed data into the database.

        Parameters
        ----------
        data : Dict[str, List[Dict[str, Any]]]
            Dictionary of tables and their rows to ingest
        """

    def _get_tables_with_constraints(self) -> list[str]:
        """Get a list of tables that have primary key or unique constraints.

        Returns
        -------
        List[str]
            List of table names with constraints
        """
        if self._tables_with_constraints is not None:
            return self._tables_with_constraints

        # Query to find tables with constraints
        query = """
            SELECT DISTINCT table_name
            FROM information_schema.table_constraints
            WHERE constraint_type IN ('PRIMARY KEY', 'UNIQUE')
            AND table_schema = 'openalex'
        """
        result = self.conn.execute(query).fetchall()
        self._tables_with_constraints = [f"openalex.{row[0]}" for row in result]
        return self._tables_with_constraints

    def _insert_dataframe(self, table_name: str, data: list[dict[str, Any]]) -> None:
        """Insert a DataFrame into a database table.

        Parameters
        ----------
        table_name : str
            The name of the table to insert into
        data : List[Dict[str, Any]]
            The data to insert
        """
        if not data:
            return

        # Check if table has constraints
        tables_with_constraints = self._get_tables_with_constraints()
        df = pl.DataFrame(data)

        # Use INSERT OR REPLACE for tables with constraints, regular INSERT otherwise
        if table_name in tables_with_constraints:
            sql = f"""
                INSERT OR REPLACE INTO {table_name}
                SELECT * FROM df
            """
        else:
            sql = f"""
                INSERT INTO {table_name}
                SELECT * FROM df
            """

        self.conn.execute(sql)
