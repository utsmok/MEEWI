import datetime
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import httpx
from pydantic import BaseModel, ValidationError

from db.duckdb import DuckDBInstance

from .mappings import ENDPOINT_TO_MESSAGECLASS, OAIREEndpoint, OAIREMessage

MAX_RESULTS = 200  # max results before storing in db


@dataclass
class OAIREFilter:
    filter_type: str  # TODO: change to OAIREFilterType
    filter_value: str | int | float | bool | list = field(default=None)

    def __str__(self) -> str:
        """
        Returns the string representation of the filter.
        """
        # TODO:: implement this
        raise NotImplementedError("OAIREFilter not yet implemented.")


@dataclass
class OAIREQuery:
    endpoint: OAIREEndpoint | str
    per_page: int | None = 50
    search_term: str | None = field(default=None)
    filters: list[OAIREFilter] | None = field(default_factory=list)
    client: httpx.Client | None = field(default=None)
    _results: list[BaseModel] | None = field(default_factory=list, init=False)
    cursor: str | None = field(default="*", init=False)
    count: int | None = field(default=None, init=False)
    total_retrieved: int = field(default=0, init=False)
    messageclass: OAIREMessage | None = field(default=None, init=False)

    def __post_init__(self) -> None:
        if isinstance(self.endpoint, str):
            try:
                self.endpoint = OAIREEndpoint(self.endpoint)
            except ValueError as e:
                raise ValueError(
                    f"Invalid endpoint: {self.endpoint}. Choose from one of the following values: {', '.join([e.value for e in OAIREEndpoint])}"
                ) from e

        self.messageclass = ENDPOINT_TO_MESSAGECLASS.get(self.endpoint)

        if self.search_term:
            self.filters.append(OAIREFilter({"search": self.search_term}))

    def get_results(self, db: DuckDBInstance | None = None) -> None:
        """
        Fetches results, stores them in db and/or in class attribute.
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
                results: OAIREMessage = self.messageclass.model_validate_json(data)

                # first time we get results, set the count
                if not self.count:
                    self.count = results.header.numfound
                    print(f"Expecting {self.count} results")

                # Check if we have received a new cursor, if not, retry
                received_cursor: str | None = results.header.nextCursor
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
                # wait 10 seconds, re-auth, and retry
                time.sleep(10)
                self._authenticate(force=True)
                repeats += 1
            except httpx.RequestError as e:
                print(f"Error fetching data for {self}: {e}")
                time.sleep(10)
                self._authenticate(force=True)
                repeats += 1
            except ValidationError as e:
                print(f"Error validating data for {self}: {e}")
                # retry once with new auth
                self._authenticate(force=True)
                if repeats >= 10:
                    break
                repeats = max(repeats + 1, 10)

        if db and self._results:
            db.store_results(self, type(self._results[0]))

        print(f"done - Retrieved {self.total_retrieved}/{self.count} results.")

    def get_url(self) -> str:
        """
        Returns the string representation of the query.
        """
        # TODO? Handle OR-ing of filters
        # now we join them with & which is "AND" in OpenAIRE
        # NOT is handled in the filter itself
        # could all OR-ing also be handled in the filter?
        filters = "&".join(map(str, self.filters)) if self.filters else ""
        if filters:
            filters = f"{filters}"
        cursor = f"cursor={self.cursor}" if self.cursor else ""
        per_page = f"pageSize={self.per_page}" if self.per_page else ""
        if any([filters, cursor, per_page]):
            params = "&".join(x for x in [filters, cursor, per_page] if x)
            return f"https://api.openaire.eu/graph/{self.endpoint.value}?{params}"
        return f"https://api.openalex.org/{self.endpoint.value}"

    def _authenticate(self, force=False) -> None:  # noqa: FBT002
        """
        adds API auth to self.client's header
        """
        if (
            self.auth_expiry_time
            and datetime.datetime.now() < self.auth_expiry_time
            and not force
        ):
            return

        if not self.client_id or not self.client_secret:
            # TODO: remove hardcoded filepath
            with Path.open("E:\MEEWI\retrieval\openaire\openaire_auth.secret") as f:
                self.client_id = f.readline().strip()
                self.client_secret = f.readline().strip()

        self.auth_expiry_time: datetime.datetime = (
            datetime.datetime.now() + datetime.timedelta(hours=1)
        )
        auth_data = httpx.post(
            url="https://aai.openaire.eu/oidc/token",
            data="grant_type=client_credentials",
            auth=httpx.BasicAuth(self.client_id, self.client_secret),
        )
        if not self.client:
            self.client = httpx.Client()
        self.client.headers["Authorization"] = (
            f"Bearer {auth_data.json()['access_token']}"
        )

    @property
    def results(self) -> list[BaseModel]:
        """
        Returns the results of the query.
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

    def store_results(self, db: DuckDBInstance) -> None:
        """
        Stores the results of the query in the DuckDB instance.
        """
        if self._results and not self.cursor:
            # if we have results and no cursor, we are done
            db.store_results(self, type(self._results[0]))
            return
        # else fetch the results and store them
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
