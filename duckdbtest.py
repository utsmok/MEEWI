import time
from dataclasses import dataclass, field
from enum import Enum
from itertools import batched

import duckdb
import httpx
import polars as pl
from pydantic import BaseModel, ValidationError
from rich import print

from openalex_schemas.create_ddl import generate_ddl
from openalex_schemas.works import Message, Work

BATCH_SIZE = 50
MAX_RESULTS = 1000


class Endpoint(Enum):
    """

    Enum for OpenAlex API endpoints.
    all have the form https://api.openalex.org/{....}
    """

    WORKS = "works"
    INSTITUTIONS = "institutions"
    AUTHORS = "authors"
    SOURCES = "sources"
    TOPICS = "topics"
    AUTOCOMPLETE = "autocomplete"
    PUBLISHERS = "publishers"
    FUNDERS = "funders"
    KEYWORDS = "keywords"
    TEXT = "text"


class OAFilterType(Enum):
    """
    Enum for OpenAlex filter types.
    """


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
class Query:
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

    def __post_init__(self) -> None:
        if isinstance(self.endpoint, str):
            try:
                self.endpoint = Endpoint(self.endpoint)
            except ValueError as e:
                raise ValueError(
                    f"Invalid endpoint: {self.endpoint}. Choose from one of the following values: {', '.join([e.value for e in Endpoint])}"
                ) from e

        if self.search_term:
            self.filters.append(OAFilter({"default.search": self.search_term}))

    def get_results(self, db: "DuckDBInstance" = None) -> None:
        """
        Fetches paginated data from OpenAlex API and stores it in the results attribute.
        """
        repeats = 0
        while self.cursor:
            try:
                data: str = self.client.get(self.get_url()).text
                results: Message = Message.model_validate_json(data)
                self._results.extend(results.results)
                self.total_retrieved += len(results.results)
                if not self.count:
                    self.count = results.meta.count
                    print(f"Expecting {self.count} results for query {self}")
                else:
                    print(
                        f"[{self.total_retrieved}/{self.count}] results retrieved & parsed"
                    )
                    if len(self._results) >= MAX_RESULTS and db:
                        print(
                            "Reached max amounts of results for a single get_results() operation. Storing data in DB and clearing self._results."
                        )
                        db.store_results(self)
                        self._results = []
                self.cursor = results.meta.next_cursor
            except httpx.HTTPStatusError as e:
                print(f"Error fetching data for {self}: {e}")
                # wait 10 seconds and retry
                time.sleep(10)
                repeats += 1
                if repeats > 5:
                    print(f"Reached max amount of retries for {self}. Stopping query.")
                    break
            except httpx.RequestError as e:
                print(f"Error fetching data for {self}: {e}")
                time.sleep(10)
                repeats += 1
                if repeats > 5:
                    print(f"Reached max amount of retries for {self}. Stopping query.")
                    break
            except ValidationError as e:
                print(f"Error validating data for {self}: {e}")
                break

        if db and self._results:
            db.store_results(self)

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


class Works(Query):
    """
    Query with the endpoint set to WORKS.
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(Endpoint.WORKS, *args, **kwargs)


@dataclass
class QuerySet:
    """
    Class that provides an abstraction layer for a set of queries.
    Requires an endpoint to be set -- each query in the set must have the same endpoint.
    """

    endpoint: Endpoint
    queries: list[Query] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.queries:
            self.queries = []

    def add(self, query: Query | list[Query]) -> None:
        """
        Adds query/queries to the set. Only accepts queries with the same endpoint as the set.
        """
        if isinstance(query, list):
            query = [q for q in query if q.endpoint == self.endpoint]
        elif query.endpoint == self.endpoint:
            query = [query]
        if query:
            self.queries.extend(query)

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


class WorksSet(QuerySet):
    """
    Queryset with the endpoint set to WORKS.
    """

    def __init__(self, queries: list[Query] | None = None) -> None:
        super().__init__(Endpoint.WORKS, queries)


class DuckDBInstance:
    """
    A class to represent a DuckDB instance.
    """

    db_name = "duck.db"

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

    def create_table(self, model: BaseModel):
        """
        Creates a table in the DuckDB instance based on the Pydantic model.
        If the table exists, this will do nothing.
        """
        if self.table_exists(model.__name__.lower()):
            print(f"Table {model.__name__} already exists in DuckDB instance.")
            return
        self.conn.execute(generate_ddl(model, table_name=model.__name__.lower()))
        print(f"Created table {model.__name__} in DuckDB instance.")

    def store_results(
        self,
        data: pl.DataFrame | Query | list[Query] | QuerySet,
        table: Endpoint | None = None,
    ) -> None:
        """
        Stores results in the DuckDB instance.

        Args:
            data: the data to store in the DuckDB instance
            table: the name of the table to store the data in
        """

        if isinstance(data, list):
            data = QuerySet(data[0].endpoint, data)

        if isinstance(data, QuerySet | Query):
            table = data.endpoint
            data = pl.from_dicts(data.serialized_results, infer_schema_length=None)

        if not table:
            raise ValueError("Table name must be provided.")
        table_name = table.value.rstrip("s")

        print(f"inserting {len(data)} items into {table_name}")

        self.conn.execute(f"""
                            INSERT OR REPLACE INTO {table_name} SELECT * FROM data;
                            """)


def get_all_ut_works(client: httpx.Client, db: DuckDBInstance):
    queryset = WorksSet()

    queryset.add(
        Query(
            endpoint=Endpoint.WORKS,
            per_page=50,
            filters=[
                OAFilter(
                    filter_type="institutions.ror",
                    filter_value="https://ror.org/006hf6230",
                ),
            ],
            email="samopsa@gmail.com",
            client=client,
        )
    )

    queryset.store_results(db)


def store_doi_data(dois: list[str], client: httpx.Client, db: DuckDBInstance) -> None:
    queryset = WorksSet()
    if len(dois) <= BATCH_SIZE:
        queryset.add(
            Query(
                endpoint=Endpoint.WORKS,
                per_page=50,
                filters=[
                    OAFilter(filter_type="doi", filter_value=dois),
                ],
                email="samopsa@gmail.com",
                client=client,
            )
        )
    else:
        queryset.add(
            [
                Query(
                    endpoint=Endpoint.WORKS,
                    per_page=50,
                    filters=[
                        OAFilter(filter_type="doi", filter_value=list(doi_batch)),
                    ],
                    email="samopsa@gmail.com",
                    client=client,
                )
                for doi_batch in batched(dois, BATCH_SIZE, strict=False)
            ]
        )
    print(len(queryset))
    db.store_results(queryset)


if __name__ == "__main__":
    # data = pl.read_csv("mor_items.csv")
    # dois = data["DOI"].to_list()
    # dois = dois[0:10]
    # print(len(dois))
    db = DuckDBInstance()
    db.create_table(Work)
    with httpx.Client() as client:
        # store_doi_data(dois, client, db)
        get_all_ut_works(client, db)
