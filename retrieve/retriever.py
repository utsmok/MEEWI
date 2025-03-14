"""
main functionality to retrieve data from various sources

user inputs an id and the retriever will return data from all valid sources for that id
"""

from collections import defaultdict

import polars as pl

from models.enums import Identifier

from .connectors import (
    Connector,
    CrossrefConnector,
    DataCiteConnector,
    OpenAIREConnector,
    OpenAlexConnector,
    ORCIDConnector,
    PubMedConnector,
    PureConnector,
)

CONNECTOR_MAPPING: dict[Identifier, list[Connector]] = {
    Identifier.DOI: [
        OpenAlexConnector,
        OpenAIREConnector,
        CrossrefConnector,
        DataCiteConnector,
        PureConnector,
    ],
    Identifier.PMID: [
        OpenAlexConnector,
        OpenAIREConnector,
        PubMedConnector,
    ],
    Identifier.ARXIV: [
        OpenAlexConnector,
        OpenAIREConnector,
    ],
    Identifier.OPENAIRE_ID: [
        OpenAIREConnector,
    ],
    Identifier.PURE_ID: [
        PureConnector,
    ],
    Identifier.ORCID: [
        OpenAlexConnector,
        OpenAIREConnector,
        ORCIDConnector,
    ],
}


def group_by_id(iterable):
    ret = defaultdict(list)
    for k in iterable:
        ret[k[0]].append(k[1])
    return dict(ret)


class Retriever:
    """
    main class to retrieve data from various sources
    usage:
    1. create the retriever instance
    2. use retriever.add_id({id_type: str, id: str}) to add an id to the retriever
    """

    def __init__(self):
        self.ids: list[tuple[Identifier, str]] = []
        self.data: dict[str, dict[str, dict]] = {}

    def add_id(self, id: tuple[Identifier, str] | list[tuple[Identifier, str]]):
        """
        add an id or list of ids to the retriever
        each id should be a tuple with the id type + id value
        """

        def check_id_type(id_type: Identifier | str) -> Identifier | None:
            if not isinstance(id_type, Identifier):
                try:
                    return Identifier(str(id_type).lower())
                except ValueError:
                    print(
                        f"Invalid id type: {id_type}. Must be one of {list(Identifier)}."
                    )
                    return None
            return id_type

        if not isinstance(id, list):
            id = [id]

        for id_tuple in id:
            id_type, id_value = id_tuple
            id_type = check_id_type(id_type)
            if id_type:
                self.ids.append((id_type, id_value))

    def retrieve(self) -> dict:
        """
        retrieve data from all sources in self.sources
        store in self.data
        then return the data
        """
        if not self.ids:
            print("No ids, nothing to retrieve")
            return {}

        full_data: dict[str, dict[str, dict]] = defaultdict(dict)
        """
        full data shape:
        {
            'input_id_1': {
                'source_1': {
                    ('key_1': 'value_1', 'key_2': 'value_2', ...),
                },
                'source_2': {
                    ('key_1': 'value_1', 'key_2': 'value_2', ...),
                },
                ...
            },
            'input_id_2': {
                'source_1': {
                    ('key_1': 'value_1', 'key_2': 'value_2', ...),
                },
                'source_2': {
                    ('key_1': 'value_1', 'key_2': 'value_2', ...),
                },
                ...
            },
            ...

        }
        """
        grouped = group_by_id(self.ids).items()

        for id_type, id_values in grouped:
            if not id_values:
                print(f"No ids for id type {id_type}.")
                continue
            connectors = CONNECTOR_MAPPING.get(id_type, None)
            if not connectors:
                print(f"No connector found for id type {id_type}.")
                continue
            for connector in connectors:
                connector_instance: Connector = connector()
                if str(connector_instance) != "OpenAlex":
                    continue
                for id_value in id_values:
                    connector_instance.add_id(id_value, id_type)
                results: dict[str, dict] = connector_instance.get()
                print(results)
                for id_value, result in results.items():
                    print(id_value, str(connector_instance))
                    full_data[id_value][str(connector_instance)] = result
                    print(full_data)

        self.data.update(full_data)
        data = dict(full_data)

        for k, v in data.items():
            if v and isinstance(v, dict):
                for source, result in v.items():
                    if len(result) == 1:
                        result = result[0]
                        if "abstract_inverted_index" in result:
                            del result["abstract_inverted_index"]
                        for key, item in result.items():
                            print(key)
                            print(f"     {item}")

                        data[k][source] = pl.from_dict(result)

        return data
