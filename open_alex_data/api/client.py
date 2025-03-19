import httpx
import polars as pl

from models.enums import EntityType


class OpenAlexClient:
    """Client to interact with the OpenAlex API."""

    BASE_URL = "https://api.openalex.org"

    def __init__(self, email=None):
        """Initialize the OpenAlex client.

        Parameters
        ----------
        email : str, optional
            Your email for polite pool access to OpenAlex API
        """
        self.headers = {}
        if email:
            self.headers["User-Agent"] = f"mailto:{email}"

    async def get_from_autocomplete(
        self,
        search_str: str,
        client: httpx.AsyncClient,
        entity_type: EntityType | str | None = None,
        autocomplete: bool = False,
    ) -> tuple[int, pl.DataFrame]:
        """Use the OA autocomplete endpoint to get suggestions for a search string.

        Parameters
        ----------
        search_str : str
            The search string to query
        client : httpx.AsyncClient
            The HTTP client to use for requests
        entity_type : EntityType | str | None, optional
            The entity type to search for, by default None
        autocomplete : bool, optional
            Whether to use the autocomplete endpoint, by default False

        Returns
        -------
        tuple[int, pl.DataFrame]
            Count of results and DataFrame of results
        """
        if isinstance(entity_type, str):
            try:
                entity_type = EntityType(entity_type)
            except ValueError:
                entity_type = None

        url = self.BASE_URL

        if not autocomplete and not entity_type:
            return 0, pl.DataFrame()

        if autocomplete:
            url += "/autocomplete"
            url += f"/{entity_type}" if entity_type else ""
            url += f"?q={search_str}"
        else:
            if not entity_type:
                return 0, pl.DataFrame()
            url += f"/{entity_type}?search={search_str}"

        print(f"Querying: {url}")
        response: httpx.Response = await client.get(url, headers=self.headers)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return 0, pl.DataFrame()

        data = response.json()
        count: int = data.get("meta", {}).get("count", 0)
        results = data.get("results", [])

        results_df = pl.from_dicts(results) if results else pl.DataFrame()
        return count, results_df
