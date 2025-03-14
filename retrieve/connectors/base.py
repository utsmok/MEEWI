"""
base classes / enums / ... for all connectors
"""

from typing import Protocol

from models.enums import Identifier


class Connector(Protocol):
    """
    Protocol for all connectors
    """

    def add_id(self, id: str, id_type: Identifier) -> None:
        """
        Add an id to the connector to retrieve data from

        :param id: the id to add
        :param id_type: the type of id to add (see Identifier enum)
        """
        ...

    def get(self, id: str | None, id_type: Identifier | None) -> dict[str, dict]:
        """
        Perform the retrieval of data for each id stored via add_id
        or; if id and id_type are provided; retrieve data for that specific id
        returns a dict with the used id as key and the retrieved data dict as value
        """
        ...

    def setup(self) -> None:
        """
        Setup the connector (e.g. set up API keys, etc.) if needed
        """
        ...


import pyalex
from pyalex import Works


class OpenAlexConnector(Connector):
    """
    Connector for OpenAlex API
    """

    def __init__(self) -> None:
        self.ids: dict[str, Identifier] = {}

    def add_id(self, id: str, id_type: Identifier) -> None:
        """
        Add an id to the connector to retrieve data from

        :param id: the id to add
        :param id_type: the type of id to add (see Identifier enum)
        """
        if id_type == Identifier.DOI:
            self.ids[id] = id_type

    def setup(self) -> None:
        """
        Setup openalex
        """
        pyalex.config.email = "mail@example.com"
        pyalex.config.max_retries = 0
        pyalex.config.retry_backoff_factor = 0.1
        pyalex.config.retry_http_codes = [429, 500, 503]

    def get(
        self, id: str | None = None, id_type: Identifier | None = None
    ) -> dict[str, dict]:
        """
        Perform the retrieval of data for each id stored via add_id
        returns a dict with the used id as key and the retrieved data dict as value
        """
        retrieval_ids: dict[str, Identifier] = {}
        if id and id_type:
            retrieval_ids[id] = id_type
        else:
            retrieval_ids = self.ids

        if not retrieval_ids:
            return {}

        self.data = {}
        for id_value, id_type in retrieval_ids.items():
            print(id_value, id_type)
            if id_type == Identifier.DOI:
                try:
                    self.data[id_value] = Works().filter(doi=id_value).get()
                except Exception as e:
                    print("Error retrieving data for DOI:", id_value)
                    print(e)
                    continue

            if id_type == Identifier.PMID:
                try:
                    self.data[id_value] = Works().filter(pmid=id_value).get()
                except Exception:
                    continue
        return self.data

    def __str__(self) -> str:
        return "OpenAlex"


class OpenAIREConnector(Connector):
    """
    Connector for OpenAIRE API
    """

    def __init__(self) -> None:
        self.ids: dict[str, Identifier] = {}
        self.data: dict[str, dict] = {}

    def add_id(self, id: str, id_type: Identifier) -> None:
        """
        Add an id to the connector to retrieve data from

        :param id: the id to add
        :param id_type: the type of id to add (see Identifier enum)
        """
        if id_type == Identifier.DOI:
            self.ids[id] = id_type


class CrossrefConnector(Connector):
    """
    Connector for Crossref API
    """

    def __init__(self) -> None:
        self.ids: dict[str, Identifier] = {}
        self.data: dict[str, dict] = {}

    def add_id(self, id: str, id_type: Identifier) -> None:
        """
        Add an id to the connector to retrieve data from

        :param id: the id to add
        :param id_type: the type of id to add (see Identifier enum)
        """
        if id_type == Identifier.DOI:
            self.ids[id] = id_type


class DataCiteConnector(Connector):
    """
    Connector for DataCite API
    """

    def __init__(self) -> None:
        self.ids: dict[str, Identifier] = {}
        self.data: dict[str, dict] = {}

    def add_id(self, id: str, id_type: Identifier) -> None:
        """
        Add an id to the connector to retrieve data from

        :param id: the id to add
        :param id_type: the type of id to add (see Identifier enum)
        """
        if id_type == Identifier.DOI:
            self.ids[id] = id_type


class PureConnector(Connector):
    """
    Connector for Pure API
    """

    def __init__(self) -> None:
        self.ids: dict[str, Identifier] = {}
        self.data: dict[str, dict] = {}

    def add_id(self, id: str, id_type: Identifier) -> None:
        """
        Add an id to the connector to retrieve data from

        :param id: the id to add
        :param id_type: the type of id to add (see Identifier enum)
        """
        if id_type == Identifier.DOI:
            self.ids[id] = id_type


class PubMedConnector(Connector):
    """
    Connector for PubMed API
    """

    def __init__(self) -> None:
        self.ids: dict[str, Identifier] = {}
        self.data: dict[str, dict] = {}

    def add_id(self, id: str, id_type: Identifier) -> None:
        """
        Add an id to the connector to retrieve data from

        :param id: the id to add
        :param id_type: the type of id to add (see Identifier enum)
        """
        if id_type == Identifier.PMID:
            self.ids[id] = id_type


class ORCIDConnector(Protocol):
    """
    Connector for ORCID API
    """

    def __init__(self) -> None:
        self.ids: dict[str, Identifier] = {}
        self.data: dict[str, dict] = {}

    def add_id(self, id: str, id_type: Identifier) -> None:
        """
        Add an id to the connector to retrieve data from

        :param id: the id to add
        :param id_type: the type of id to add (see Identifier enum)
        """
        if id_type == Identifier.ORCID:
            self.ids[id] = id_type
