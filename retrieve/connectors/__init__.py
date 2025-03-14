"""
this module contains the connectors for the different retrieval systems
each one a class that implements the same interface
"""

from .base import (
    Connector,
    CrossrefConnector,
    DataCiteConnector,
    OpenAIREConnector,
    OpenAlexConnector,
    ORCIDConnector,
    PubMedConnector,
    PureConnector,
)

__all__: list[Connector] = [
    OpenAlexConnector,
    OpenAIREConnector,
    CrossrefConnector,
    DataCiteConnector,
    PureConnector,
    PubMedConnector,
    ORCIDConnector,
]
