from dataclasses import dataclass, field
from typing import Self

import httpx
from pydantic import BaseModel, ValidationError
from rich import print
from .mappings import OAIREEndpoint
from db.duckdb import DuckDBInstance

@dataclass
class OAIREFilter:
    filter_type: str  # TODO: implement & change to OAIREFilterType
    filter_value: str | int | float | bool | list = field(default=None)

@dataclass
class OAIREQuery:

    endpoint: OAIREEndpoint | str
    per_page: int | None = 50
    search_term: str | None = field(
        default=None
    )
    filters: list[OAIREFilter] | None = field(default_factory=list)
    client: httpx.Client | None = field(default=None)
    _results: list[BaseModel] | None = field(default_factory=list, init=False)
    cursor: str | None = field(default="*", init=False)
    count: int | None = field(default=None, init=False)
    total_retrieved: int = field(default=0, init=False)

    #TODO: Implement this class

    # don't forget auth methods, include in client header

    def get_results(self, db: DuckDBInstance | None = None) -> None:
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

    def store_results(self, db: DuckDBInstance) -> None:
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
class OAIREQuerySet:
    endpoint: OAIREEndpoint
    queries: list[OAIREQuery] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.queries:
            self.queries = []

    def add(self, query: OAIREQuery | list[OAIREQuery]) -> Self:
        """
        Adds query/queries to the set. Only accepts queries with the same endpoint as the set.
        """
        if isinstance(query, list):
            query = [q for q in query if q.endpoint == self.endpoint]
        elif query.endpoint == self.endpoint:
            query = [query]
        if query:
            self.queries.extend(query)
        return self

    @property
    def results(self) -> list[BaseModel]:
        """
        Returns the results of all queries in the set as a list of pydantic models.
        """
        results = []
        for query in self.queries:
            results.extend(query.results)
        return results

    @property
    def serialized_results(self) -> list[dict]:
        """
        Returns the results of all queries in the set as a list of dictionaries.
        """
        results = []
        for query in self.queries:
            results.extend(query.serialized_results)
        return results

    def store_results(self, db: "DuckDBInstance") -> None:
        """
        Stores the results of all queries in the set in the DuckDB instance.
        """
        if not self.queries:
            raise ValueError("No queries in the set.")
        for query in self.queries:
            query.store_results(db)



    def __len__(self) -> int:
        """
        Returns the number of queries in the set.
        """
        return len(self.queries)


