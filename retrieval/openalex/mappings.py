"""

Various enums, functions, mappings, etc for retrieval from the OpenAlexAPI.
"""

from enum import Enum
from typing import Protocol

from .models import (
    AuthorMessage,
    FunderMessage,
    InstitutionMessage,
    PublisherMessage,
    SourceMessage,
    TopicMessage,
    WorkMessage,
)


class OAEndpoint(Enum):
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


ENDPOINT_TO_MESSAGECLASS: dict[OAEndpoint, "OAMessage"] = {
    OAEndpoint.WORKS: WorkMessage,
    OAEndpoint.INSTITUTIONS: InstitutionMessage,
    OAEndpoint.AUTHORS: AuthorMessage,
    OAEndpoint.SOURCES: SourceMessage,
    OAEndpoint.TOPICS: TopicMessage,
    OAEndpoint.PUBLISHERS: PublisherMessage,
    OAEndpoint.FUNDERS: FunderMessage,
}

ID_TO_ENDPOINT: dict[str, OAEndpoint] = {
    "S": OAEndpoint.SOURCES,
    "https://openalex.org/S": OAEndpoint.SOURCES,
    "P": OAEndpoint.PUBLISHERS,
    "https://openalex.org/P": OAEndpoint.PUBLISHERS,
    "I": OAEndpoint.INSTITUTIONS,
    "https://openalex.org/I": OAEndpoint.INSTITUTIONS,
    "A": OAEndpoint.AUTHORS,
    "https://openalex.org/A": OAEndpoint.AUTHORS,
    "T": OAEndpoint.TOPICS,
    "https://openalex.org/T": OAEndpoint.TOPICS,
    "F": OAEndpoint.FUNDERS,
    "https://openalex.org/F": OAEndpoint.FUNDERS,
    "W": OAEndpoint.WORKS,
    "https://openalex.org/W": OAEndpoint.WORKS,
}


class OAResult(Protocol):
    id: str | None = None
    display_name: str | None = None
    ...


class OAMeta(Protocol):
    count: int | None = None
    q: str | None = None
    db_response_time_ms: int | None = None
    page: int | None = None
    per_page: int | None = None
    next_cursor: str | None = None
    groups_count: int | None = None
    apc_list_sum_usd: int | None = None
    apc_paid_sum_usd: int | None = None
    cited_by_count_sum: int | None = None


class OAMessage(Protocol):
    results: list[OAResult]
    meta: OAMeta | None = None
