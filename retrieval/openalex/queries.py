import time
from dataclasses import dataclass, field
from itertools import batched
from typing import Self

import httpx
from pydantic import BaseModel, ValidationError
from rich import print

from db.duckdb import DuckDBInstance

from .utils import ENDPOINT_TO_MESSAGECLASS, BaseMessage, Endpoint

BATCH_SIZE = 50
MAX_RESULTS = 200


@dataclass
class OAFilter:
    """
    A class to represent an OpenAlex filter.
    Will be used to create filterstrings for the OpenAlex API.
    """

    filter_type: str  # TODO: implement & change to OAFilterType
    filter_value: str | int | float | bool | list = field(default=None)
    # use a str as value to include parameters, e.g. ! for not, > for greater than, < for less than, etc.
    use_or: bool = field(
        default=False,
        metadata={
            "help": "If true, will use pipes (|) to join multiple filter values."
        },
    )

    def __str__(self) -> str:
        """
        Returns the string representation of the filter.
        """
        if self.filter_type == "doi" and isinstance(self.filter_value, list):
            self.use_or = True

        if isinstance(self.filter_value, dict):
            # flatten in some way -- for nested filters
            ...
        elif isinstance(self.filter_value, list):
            if self.use_or:
                self.filter_value = "|".join(map(str, self.filter_value))
            else:
                return_val = ""
                for value in self.filter_value:
                    return_val += str(self.filter_type) + ":" + str(value) + ","
                return return_val[:-1]

        elif isinstance(self.filter_value, bool):
            self.filter_value = str(self.filter_value).lower()

        return self.filter_type + ":" + str(self.filter_value)


@dataclass
class OAQuery:
    """
    Class to represent a query to the OpenAlex API.
    Initialize with a endpoint
    """

    endpoint: Endpoint | str
    per_page: int | None = 50  # between 1 and 200
    search_term: str | None = field(
        default=None
    )  # will be used to create filter {"default.search": search_term}
    filters: list[OAFilter] | None = field(default_factory=list)
    email: str | None = field(
        default=None, metadata={"help": "Email address for OpenAlex API polite pool."}
    )
    client: httpx.Client | None = field(default=None)
    _results: list[BaseModel] | None = field(default_factory=list, init=False)
    cursor: str | None = field(default="*", init=False)
    count: int | None = field(default=None, init=False)
    total_retrieved: int = field(default=0, init=False)
    messageclass: BaseMessage | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        if isinstance(self.endpoint, str):
            try:
                self.endpoint = Endpoint(self.endpoint)
            except ValueError as e:
                raise ValueError(
                    f"Invalid endpoint: {self.endpoint}. Choose from one of the following values: {', '.join([e.value for e in Endpoint])}"
                ) from e

        self.messageclass = ENDPOINT_TO_MESSAGECLASS.get(self.endpoint)

        if self.search_term:
            self.filters.append(OAFilter({"default.search": self.search_term}))

    def get_results(self, db: "DuckDBInstance" = None) -> None:
        """
        Fetches paginated data from OpenAlex API and stores it in the results attribute.
        """
        repeats = 0

        while self.cursor:
            if repeats > 10:
                print(
                    f"Reached max amount of retries for {self}. Stopping query retrieval."
                )
                break

            try:
                # Fetch from API
                data: str = self.client.get(self.get_url()).text
                results: BaseMessage = self.messageclass.model_validate_json(data)

                # first time we get results, set the count
                if not self.count:
                    self.count = results.meta.count
                    print(f"Expecting {self.count} results for query {self}")

                # Check if we have received a new cursor, if not, retry
                received_cursor: str | None = results.meta.next_cursor
                if (
                    not received_cursor
                    and self.total_retrieved + len(results.results) < self.count
                ):
                    print(
                        f"Did not receive new cursor, but {self.count - self.total_retrieved} results are still expected. Retrying this query.."
                    )
                    time.sleep(5)
                    repeats += 1
                    continue

                # Update cursor, results and amount retrieved
                print(f"[{self.total_retrieved}/{self.count}]")
                self.cursor = received_cursor
                self._results.extend(results.results)
                self.total_retrieved += len(results.results)
                if len(self._results) >= MAX_RESULTS and db:
                    db.store_results(self, type(self._results[0]))
                    self._results = []

            except httpx.HTTPStatusError as e:
                print(f"Error fetching data for {self}: {e}")
                # wait 10 seconds and retry
                time.sleep(10)
                repeats += 1
            except httpx.RequestError as e:
                print(f"Error fetching data for {self}: {e}")
                time.sleep(10)
                repeats += 1
            except ValidationError as e:
                print(f"Error validating data for {self}: {e}")
                break

        if db and self._results:
            db.store_results(self, type(self._results[0]))

        print(f"done - Retrieved {self.total_retrieved}/{self.count} results.")

    def get_url(self) -> str:
        """
        Returns the string representation of the query.
        """

        filters = ",".join(map(str, self.filters)) if self.filters else ""
        if filters:
            filters = f"filter={filters}"
        cursor = f"cursor={self.cursor}" if self.cursor else ""
        per_page = f"per_page={self.per_page}" if self.per_page else ""
        mailto = f"mailto={self.email}" if self.email else ""
        if any([filters, cursor, per_page, mailto]):
            params = "&".join(x for x in [filters, cursor, per_page, mailto] if x)
            return f"https://api.openalex.org/{self.endpoint.value}?{params}"
        return f"https://api.openalex.org/{self.endpoint.value}"

    @property
    def results(self) -> list[BaseModel]:
        """
        Returns the results of the query as a list of pydantic models.
        """
        if not self._results:
            self.get_results()
        return self._results

    @property
    def serialized_results(self) -> list[dict]:
        """
        Returns the results of the query as a list of dictionaries.
        """
        if not self._results:
            self.get_results()
        return [result.model_dump() for result in self._results]

    def store_results(self, db: "DuckDBInstance") -> None:
        """
        Stores the results of the query in the DuckDB instance.
        """
        self.get_results(db)

    def __len__(self) -> int:
        """
        Returns the number of results in the query.
        """
        if not self.count:
            self.get_results()
        return self.count

    def __str__(self) -> str:
        """
        Returns the string representation of the query.
        """
        return self.get_url()


class OAWorks(OAQuery):
    """
    Convenience class for the OpenAlex API query.
    Identical to a Query class, just with the endpoint set to WORKS.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(Endpoint.WORKS, *args, **kwargs)


@dataclass
class OAQuerySet:
    """
    Class that provides an abstraction layer for a set of queries.
    Requires an endpoint to be set -- each query in the set must have the same endpoint.
    """

    endpoint: Endpoint
    queries: list[OAQuery] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.queries:
            self.queries = []

    def add(self, query: OAQuery | list[OAQuery]) -> Self:
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

    def add_id_batch(self, ids: list[str], id_type: str) -> Self:
        """
        For a list of ids and a given id_type, create queries that concat 50 ids at a time and add them to the set.

        TODO: turn id_type into an Enum
        """
        BATCH_SIZE = 50
        client = httpx.Client()

        for id_batch in batched(ids, BATCH_SIZE, strict=False):
            self.add(
                OAQuery(
                    endpoint=self.endpoint,
                    per_page=50,
                    filters=[
                        OAFilter(filter_type=id_type, filter_value=list(id_batch)),
                    ],
                    email="samopsa@gmail.com",
                    client=client,
                )
            )
        return self

    def __len__(self) -> int:
        """
        Returns the number of queries in the set.
        """
        return len(self.queries)


class OAWorksSet(OAQuerySet):
    """
    Queryset with the endpoint set to WORKS.
    """

    def __init__(self, queries: list[OAQuery] | None = None) -> None:
        super().__init__(Endpoint.WORKS, queries)
