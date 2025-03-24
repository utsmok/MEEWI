import time
import traceback

import httpx
from pydantic import BaseModel

from db.duckdb import DuckDBInstance

from .mappings import (
    ENDPOINT_METADATA_PREFIX,
    ENDPOINT_TO_COLLECTION,
    ENDPOINT_TO_MODEL,
    PureEndpoint,
    parse_raw_pure_data,
)


class PureRetriever:
    """
    class to retrieve data from the oai-pmh endpoint of UT's Pure repo.
    very simple class, as we'll just fetch the complete contents of the selected endpoint and store it in the db
    storage is handled by a DBInstance class, and parsing of xml by the various models.
    """

    _results: list[BaseModel] = []
    total: int = 0

    def __init__(
        self, endpoint: PureEndpoint, client: httpx.Client | None = None
    ) -> None:
        self.endpoint = endpoint
        self.collection = ENDPOINT_TO_COLLECTION.get(endpoint)
        self.prefix = ENDPOINT_METADATA_PREFIX.get(endpoint)
        self.basemodel: BaseModel = ENDPOINT_TO_MODEL.get(endpoint)
        self.url = f"https://ris.utwente.nl/ws/oai?verb=ListRecords&set={self.collection}&metadataPrefix={self.prefix}"
        self.client = client or httpx.Client()

    def get_and_store_data(self, db: DuckDBInstance, batch=100) -> None:
        resumptionToken = "initial"
        batchno = 0
        ids_stored = None
        print(f"Fetching {self.collection} data from Pure...")
        while resumptionToken:
            if resumptionToken != "initial":
                self.url = f"https://ris.utwente.nl/ws/oai?verb=ListRecords&resumptionToken={resumptionToken}"
            try:
                data = self.client.get(self.url).text
            except httpx.ReadTimeout as e:
                print(f"Request timed out: {e}")
                print("Waiting for 5 seconds before retrying...")
                time.sleep(5)
                continue
            except httpx.RequestError as e:
                print(f"An error occurred while fetching data: {e}")
                print(f"Traceback: {traceback.format_exc()}")
                return

            batchno += 1

            resumptionToken, parsed_items = parse_raw_pure_data(
                data, self.endpoint, ids_stored
            )

            self.total += len(parsed_items)
            print(f"{self.total} [+{len(parsed_items)}]")

            self._results.extend(parsed_items)

            if len(self._results) > batch:
                ids_stored = db.store_results(
                    self,
                    model=self.basemodel,
                )
                self._results = []

        print(f"{self.total} items fetched")

    @property
    def results(self) -> list:
        """
        returns the results of the last fetch
        """
        return self._results

    @property
    def serialized_results(self) -> list[dict]:
        """
        returns the results of the last fetch as a list of dicts
        """
        return [item.model_dump() for item in self._results]
