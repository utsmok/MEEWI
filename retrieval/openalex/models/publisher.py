from typing import Any

from pydantic import BaseModel, Field, model_validator

"""
This module contains the Pydantic models for parsing & validation OpenAlex API responses from the '/publishers' endpoint.
The models are designed to be used with the OpenAlex API and are structured to match the expected JSON response format.
"""


class CountsByYear(BaseModel):
    year: int | None = None
    works_count: int | None = None
    cited_by_count: int | None = None

    class Config:
        frozen = True


class Role(BaseModel):
    role: str | None = None
    id: str | None = None
    works_count: int | None = None

    class Config:
        frozen = True


class XConcepts(BaseModel):
    id: str | None = None
    wikidata: str | None = None
    display_name: str | None = None
    level: int | None = None
    score: float | None = None

    class Config:
        frozen = True


class SummaryStats(BaseModel):
    two_year_mean_citedness: float | None = Field(None, alias="2yr_mean_citedness")
    h_index: int | None = None
    i10_index: int | None = None

    class Config:
        frozen = True
        populate_by_name = True


class TopicHierarchy(BaseModel):
    id: str | None = None
    display_name: str | None = None

    class Config:
        frozen = True


class Topic(BaseModel):
    id: str | None = None
    display_name: str | None = None
    count: int | None = None
    value: float | None = None
    score: float | None = None
    subfield: TopicHierarchy | None = None
    field: TopicHierarchy | None = None
    domain: TopicHierarchy | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        """
        Replace None values with empty class instances for nested fields
        """
        if not isinstance(data, dict):
            return data

        for field in ["subfield", "field", "domain"]:
            if data.get(field) is None:
                data[field] = TopicHierarchy()

        return data

    class Config:
        frozen = True


class Meta(BaseModel):
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

    class Config:
        frozen = True


class IDs(BaseModel):
    openalex: str | None = None
    ror: str | None = None
    wikidata: str | None = None

    class Config:
        extra = "allow"
        frozen = True


class ParentPublisher(BaseModel):
    id: str | None = None
    display_name: str | None = None
    ids: IDs | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        """
        Replace None values with empty class instances for nested fields
        """
        if not isinstance(data, dict):
            return data

        if data.get("ids") is None:
            data["ids"] = IDs()

        return data

    class Config:
        frozen = True


class Publisher(BaseModel):
    id: str | None = None
    display_name: str | None = None
    alternate_titles: list[str] = Field(default_factory=list)
    hierarchy_level: int | None = None
    parent_publisher: ParentPublisher | None = None
    lineage: list[str] = Field(default_factory=list)
    country_codes: list[str] = Field(default_factory=list)
    homepage_url: str | None = None
    image_url: str | None = None
    image_thumbnail_url: str | None = None
    works_count: int | None = None
    cited_by_count: int | None = None
    summary_stats: SummaryStats | None = None
    ids: IDs | None = None
    counts_by_year: list[CountsByYear] = Field(default_factory=list)
    roles: list[Role] = Field(default_factory=list)
    sources_api_url: str | None = None
    updated_date: str | None = None
    created_date: str | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        """
        Replace None values with empty class instances for nested fields
        """
        if not isinstance(data, dict):
            return data

        if data.get("parent_publisher") is None:
            data["parent_publisher"] = ParentPublisher()

        if data.get("summary_stats") is None:
            data["summary_stats"] = SummaryStats()

        if data.get("ids") is None:
            data["ids"] = IDs()

        for field in ["counts_by_year", "roles"]:
            if not data.get(field) or data[field] is None:
                data[field] = []

        return data

    class Config:
        frozen = True


class Message(BaseModel):
    meta: Meta | None = None
    results: list[Publisher] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        """
        Replace None values with empty class instances for nested fields
        """
        if not isinstance(data, dict):
            return data

        if data.get("meta") is None:
            data["meta"] = Meta()

        if not data.get("results") or data["results"] is None:
            data["results"] = []

        return data

    class Config:
        frozen = True
