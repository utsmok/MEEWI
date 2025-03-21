from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol

import httpx
from pydantic import BaseModel

from db.base import DBInstance


@dataclass
class BaseFilter(Protocol):
    """
    Base class for filters used in queries.
    """

    filter_type: Enum
    filter_value: str | int | float | bool | list = field(default=None)

    def __str__(self) -> str:
        """
        Returns the string representation of the filter.
        """


@dataclass
class BaseQuery(Protocol):
    endpoint: Enum | str
    per_page: int | None = field(default=None)
    search_term: str | None = field(default=None)
    filters: list[BaseFilter] | None = field(default_factory=list)
    client: httpx.Client | None = field(default=None)
    _results: list[BaseModel] | None = field(default_factory=list, init=False)
    cursor: str | None = field(default="*", init=False)
    count: int | None = field(default=None, init=False)
    total_retrieved: int = field(default=0, init=False)

    def get_results(self, db: DBInstance | None = None) -> None:
        """
        Fetches results, stores them in db and/or in class attribute.
        """

    def get_url(self) -> str:
        """
        Returns the string representation of the query.
        """

    @property
    def results(self) -> list[BaseModel]:
        """
        Returns the results of the query.
        """

    @property
    def serialized_results(self) -> list[dict]:
        """
        Returns the results of the query as a list of dictionaries.
        """

    def store_results(self, db: DBInstance) -> None:
        """
        Stores the results of the query in the DuckDB instance.
        """

    def __len__(self) -> int:
        """
        Returns the number of results in the query.
        """

    def __str__(self) -> str:
        """
        Returns the string representation of the query.
        """
        return self.get_url()


@dataclass
class BaseQuerySet(Protocol):
    """
    Protocol for classes that hold & control sets of queries.
    Requires an endpoint to be set, and each query in the set must have the same endpoint.
    """
    endpoint: Enum | str
    queries: list[BaseQuery] = field(default_factory=list)

    def add(self, query: BaseQuery | list[BaseQuery]) -> None:
        """
        Adds query/queries to the set. Only accepts queries with the same endpoint as the set.
        """

    @property
    def results(self) -> list[BaseModel]:
        """
        Returns the results of all queries in the set as a list of pydantic models.
        """

    @property
    def serialized_results(self) -> list[dict]:
        """
        Returns the results of all queries in the set as a list of dictionaries.
        """

    def store_results(self, db: DBInstance) -> None:
        """
        Stores the results of all queries in the set in the DuckDB instance.
        """

    def __len__(self) -> int:
        """
        Returns the number of queries in the set.
        """

class BaseEnricher(Protocol):
    """
    Protocol for classes that enrich existing data stored in a 'DB' instance with additional data from an API.
    Contains methods that e.g.
    -> create a queryset for a given set of input, filters, and/or itemtypes
    -> create a queryset based on a db instance + tablename + field + endpoint or something similar
    """

    db: DBInstance
    queryset: dict[str|Enum, BaseQuerySet] = field(default_factory=dict, init=False)

    def retrieve_related_items(self, table_name: str) -> None:
        """
        For a given table name in the DB instance,
        retrieve all fields in the table that hold a retrievable id, and then retrieve them using a queryset.
        """