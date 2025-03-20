from typing import Any, Protocol

from pydantic import BaseModel


class DBInstance(Protocol):
    db_name: str

    @property
    def conn(self) -> Any:
        """
        Returns the connection to the db.
        """

    def __enter__(self) -> Any:
        """
        Returns the connection to the db.
        for use as context manager
        """

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Closes the connection to the db.
        for use as context manager
        """

    def table_exists(self, table_name: str) -> bool:
        """
        Checks if a table exists in this db instance.
        """

    def clear_table(self, table_name: str) -> None:
        """
        Clears a table in the DB instance.
        """

    def create_table(self, model: BaseModel, tablename: str | None = None):
        """
        Creates a table in the db instance based on the Pydantic model.
        If the table exists, this will do nothing.
        """

    def retrieve_ids(self, table_name: str) -> None:
        """
        retrieve all ids from a table
        store in self.ids[table_name]=set()
        use to avoid insertions of duplicates
        """

    def store_results(
        self,
        data: Any,
    ) -> None:
        """
        Stores results in the DB instance.

        Args:
            data: the data to store in the DB instance, in Query or QuerySet format
        """
