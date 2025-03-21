from enum import Enum

import duckdb
import polars as pl
from pydantic import BaseModel

from retrieval.base_classes import BaseQuery, BaseQuerySet
from utils.create_ddl import generate_ddl


class DuckDBInstance:
    """
    A class to represent a DuckDB instance.
    """

    db_name = "duck.db"
    ids = {}

    def __init__(self, db_name: str = "duck.db") -> None:
        self.db_name = db_name
        self.connection = duckdb.connect(database=self.db_name)

    @property
    def conn(self) -> duckdb.DuckDBPyConnection:
        """
        Returns the connection to the DuckDB instance.
        """
        if not self.connection:
            self.connection = duckdb.connect(self.db_name)
        return self.connection

    def __enter__(self) -> duckdb.DuckDBPyConnection:
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.connection.close()

    def table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in the DuckDB instance.
        """
        result = self.conn.execute(
            f"SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{table_name}';"
        ).fetchone()
        return result[0] > 0

    def clear_table(self, table_name: str = "openalex_data") -> None:
        """
        Clears a table in the DuckDB instance.
        """

        self.conn.execute(f"DROP TABLE IF EXISTS {table_name};")

    def create_table(self, model: BaseModel | None, tablename: str | None = None):
        """
        Creates a table in the DuckDB instance based on the Pydantic model.
        If the table exists, this will do nothing.
        """
        if not tablename:
            tablename = model.__name__.lower()
        if self.table_exists(tablename):
            print(f"Table {tablename} already exists in DuckDB instance.")
            return
        self.conn.execute(generate_ddl(model, table_name=tablename))
        print(f"Created table {tablename} in DuckDB instance.")

    def retrieve_ids(self, table_name: str) -> set[str]:
        """
        retrieve all openalex ids from a table, eg works
        store in self.ids[table_name]=set()
        use to avoid insertions of duplicates
        """
        if not self.table_exists(table_name):
            print(f'Table {table_name} does not exist in DuckDB instance.')
            return set()


        self.conn.execute(f"SELECT id FROM {table_name};")
        ids = self.conn.fetchall()
        ids = [id[0] for id in ids]
        self.ids[table_name] = set(ids)
        print(f"Retrieved {len(ids)} ids from {table_name} table.")
        return self.ids[table_name]
    def store_results(
        self,
        query_input: BaseQuery | BaseQuerySet,
        model: BaseModel | None = None,
    ) -> None:
        """
        Stores results in the DuckDB instance.

        Args:
            data: the data to store in the DuckDB instance
            table: the name of the table to store the data in
        """
        try:
            table = query_input.endpoint
            data: pl.DataFrame = pl.from_dicts(
                query_input.serialized_results, infer_schema_length=None
            )
        except AttributeError as err:
            raise ValueError("Data must be in Query or QuerySet format.") from err

        if not table:
            raise ValueError("Input data has no endpoint attribute.")
        if isinstance(table, str):
            table_name = table.rstrip("s")
        elif isinstance(table, Enum):
            table_name = table.value.rstrip("s")
        if not self.table_exists(table_name):
            self.create_table(model=model, tablename=table_name)
        if table_name not in self.ids:
            self.retrieve_ids(table_name)

        data = data.filter(pl.col("id").is_in(self.ids[table_name]).not_())
        if data.is_empty():
            print(f"No new data to insert into {table_name}.")
            return
        print(f"inserting {len(data)} items into {table_name}")
        try:
            self.conn.register("data_view", data)
        except Exception as e:
            print(f"Error inserting data into {table_name}: {e}")
            return
        try:
            self.conn.execute(f"""
                              INSERT INTO {table_name} SELECT * FROM data_view;
                            """)

            self.conn.execute("DROP VIEW IF EXISTS data_view")
        except Exception as e:
            print(f"Error inserting data into {table_name}: {e}")
            return
        print(f"Done inserting {len(data)} items into {table_name}")
        self.retrieve_ids(table_name)
