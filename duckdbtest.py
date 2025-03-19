import contextlib
from dataclasses import dataclass, field
from enum import Enum
from itertools import batched

import duckdb
import httpx
import polars as pl

BATCH_SIZE = 50


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
    _results: list[dict] | None = field(default_factory=list, init=False)
    cursor: str | None = field(default="*", init=False)

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

    def _parse_results(self, results: list[dict]) -> None:
        """
        Private method to parse the results of the query and store them in the results attribute.
        It will also invert the abstract_inverted_index to the actual abstract if present (for Works).
        """
        if not results:
            return
        if not self._results:
            self._results = []
        if self.endpoint == Endpoint.WORKS:
            for result in results:
                with contextlib.suppress(KeyError):
                    result["abstract"] = invert_abstract(
                        result.get("abstract_inverted_index", {})
                    )
                    del result["abstract_inverted_index"]
        self._results.extend(results)

    def get_results(self) -> None:
        """
        Fetches paginated data from OpenAlex API and stores it in the results attribute.
        """
        while self.cursor:
            data: dict[str, list[dict] | dict[int | str]] = self.client.get(
                self.get_url()
            ).json()
            self._parse_results(data.get("results", []))
            self.cursor = data.get("meta", {}).get("next_cursor")

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
    def results(self) -> list[dict]:
        """
        Returns the results of the query.
        """
        if not self._results:
            self.get_results()
        return self._results


class DuckDBInstance:
    """
    A class to represent a DuckDB instance.
    """

    db_name = "duck.db"

    def __init__(self, db_name: str = "duck.db") -> None:
        self.db_name = db_name
        self.conn = duckdb.connect(database=self.db_name)

    def __enter__(self) -> duckdb.DuckDBPyConnection:
        if not self.conn:
            self.conn = duckdb.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.close()

    def clear_table(self, table_name: str = "openalex_data") -> None:
        """
        Clears a table in the DuckDB instance.
        """
        if not self.conn:
            self.conn = duckdb.connect(self.db_name)
        self.conn.execute(f"DROP TABLE IF EXISTS {table_name};")

    def store_results(
        self, data: pl.DataFrame | Query | list[Query], table: Endpoint | None = None
    ) -> None:
        """
        Stores results in the DuckDB instance.

        Args:
            data: the data to store in the DuckDB instance
            table: the name of the table to store the data in
        """
        if not self.conn:
            self.conn = duckdb.connect(self.db_name)
        if isinstance(data, Query):
            table = data.endpoint
            data = pl.from_dicts(data.results)
        elif isinstance(data, list):
            table = data[0].endpoint
            full_results = []
            for query in data:
                full_results.extend(query.results)
            data = pl.from_dicts(full_results, infer_schema_length=None)
        if not table:
            raise ValueError("Table name must be provided.")
        print(f"inserting {len(data)} items into {table.value}")

        tables_present = self.conn.execute("SELECT * FROM duckdb_tables();").fetchall()
        table_names = [t[4] for t in tables_present]
        print(table_names)
        print(table.value)
        print(table.value in table_names)
        if table.value in table_names:
            self.conn.execute(f"""
                            INSERT OR REPLACE INTO {table.value} SELECT * FROM data;
                            """)
        else:
            self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {table.value} AS
            SELECT * FROM data;
            """)


def invert_abstract(inverted_abstract: dict[str, list[int]]) -> str:
    """
    takes a dictionary of inverted indexes and returns the abstract as a string
    """
    if not inverted_abstract:
        return None
    l_inv = [(w, p) for w, pos in inverted_abstract.items() for p in pos]
    return " ".join(map(lambda x: x[0], sorted(l_inv, key=lambda x: x[1])))


def store_doi_data(dois: list[str], client: httpx.Client, db: DuckDBInstance) -> None:
    queries: list[Query] = []
    if len(dois) <= BATCH_SIZE:
        queries.append(
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
        queries.extend(
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
    print(len(queries))
    db.store_results(queries)


if __name__ == "__main__":
    data = pl.read_csv("mor_items.csv")
    dois = data["DOI"].to_list()
    print(len(dois))
    db = DuckDBInstance()
    with httpx.Client() as client:
        store_doi_data(dois, client, db)
