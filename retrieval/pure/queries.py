import httpx

from db.duckdb import DuckDBInstance

from .mappings import ENDPOINT_TO_COLLECTION, PureEndpoint


class PureRetriever:
    """
    class to retrieve data from the oai-pmh endpoint of UT's Pure repo.
    very simple class, as we'll just fetch the complete contents of the selected endpoint and store it in the db
    storage is handled by a DBInstance class, and parsing of xml by the various models.
    """

    def __init__(
        self, endpoint: PureEndpoint, client: httpx.Client | None = None
    ) -> None:
        self.endpoint = endpoint
        self.collection = ENDPOINT_TO_COLLECTION.get(endpoint)
        self.url = f"https://ris.utwente.nl/ws/oai?verb=ListRecords&set={self.collection}&metadataPrefix=mods"
        self.client = client or httpx.Client()

    def get_and_store_data(self, db: DuckDBInstance, batch=100) -> None:
        resumetoken = "initial"
        results = []
        while resumetoken:
            data = self.client.get(self.url)
            # parse the XML response using the appropriate model
            # add the results to 'results'

            # get the resumption token
            # resumetoken = data.resumption_token

            if len(results) > batch:
                db.store_results(results)
                results = []
