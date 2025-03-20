from typing import Any

from pydantic import BaseModel, Field, model_validator

"""
This module contains the Pydantic models for parsing & validation OpenAlex API responses from the '/topics' endpoint.
The models are designed to be used with the OpenAlex API and are structured to match the expected JSON response format.
"""


class TopicHierarchy(BaseModel):
    id: str | None = None
    display_name: str | None = None

    class Config:
        frozen = True


class IDs(BaseModel):
    openalex: str | None = None
    wikipedia: str | None = None

    class Config:
        frozen = True


class Topic(BaseModel):
    id: str | None = None
    display_name: str | None = None
    description: str | None = None
    keywords: list[str] = Field(default_factory=list)
    ids: IDs | None = None
    subfield: TopicHierarchy | None = None
    field: TopicHierarchy | None = None
    domain: TopicHierarchy | None = None
    siblings: list[TopicHierarchy] = Field(default_factory=list)
    works_count: int | None = None
    cited_by_count: int | None = None
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

        if data.get("ids") is None:
            data["ids"] = IDs()

        if data.get("subfield") is None:
            data["subfield"] = TopicHierarchy()

        if data.get("field") is None:
            data["field"] = TopicHierarchy()

        if data.get("domain") is None:
            data["domain"] = TopicHierarchy()

        if not data.get("siblings") or data["siblings"] is None:
            data["siblings"] = []

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


class Message(BaseModel):
    meta: Meta | None = None
    results: list[Topic] = Field(default_factory=list)

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
