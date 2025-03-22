from enum import Enum
from typing import Protocol

from .models import (
    ResearchProductMessage,
)


class OAIREEndpoint(Enum):
    RESEARCHPRODUCTS = "researchProducts"
    ORGANIZATIONS = "organizations"
    DATASOURCES = "dataSources"
    PROJECTS = "projects"


class OAIREFilterType(Enum):
    """
    Enum for OpenAIRE filter types.
    """


class OAIREHeader(Protocol):
    numfound: int
    maxscore: int | None
    querytime: int
    page: int
    pageSize: int | None
    nextCursor: str | None


class OAIREResult(Protocol):
    id: str


class OAIREMessage(Protocol):
    header: OAIREHeader
    results: list[OAIREResult]


ENDPOINT_TO_MESSAGECLASS: dict[OAIREEndpoint, OAIREMessage] = {
    OAIREEndpoint.RESEARCHPRODUCTS: ResearchProductMessage,
    OAIREEndpoint.ORGANIZATIONS: "OrganizationMessage",
    OAIREEndpoint.DATASOURCES: "DataSourceMessage",
    OAIREEndpoint.PROJECTS: "ProjectMessage",
}
