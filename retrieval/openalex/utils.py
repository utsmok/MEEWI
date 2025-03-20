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


ENDPOINT_TO_MESSAGECLASS: dict[Endpoint, "BaseMessage"] = {
    Endpoint.WORKS: WorkMessage,
    Endpoint.INSTITUTIONS: InstitutionMessage,
    Endpoint.AUTHORS: AuthorMessage,
    Endpoint.SOURCES: SourceMessage,
    Endpoint.TOPICS: TopicMessage,
    Endpoint.PUBLISHERS: PublisherMessage,
    Endpoint.FUNDERS: FunderMessage,
}


class BaseResult(Protocol):
    id: str | None = None
    display_name: str | None = None
    ...


class Meta(Protocol):
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


class BaseMessage(Protocol):
    results: list[BaseResult]
    meta: Meta | None = None
