from typing import Any

from pydantic import BaseModel, Field, model_validator

"""
This module contains the Pydantic models for parsing & validation OpenAlex API responses from the '/institutions' endpoint.
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


class InstitutionType(BaseModel):
    id: str | None = None
    display_name: str | None = None
    description: str | None = None
    works_count: int | None = None
    cited_by_count: int | None = None
    works_api_url: str | None = None
    updated_date: str | None = None
    created_date: str | None = None

    class Config:
        frozen = True


class IDs(BaseModel):
    openalex: str | None = None
    ror: str | None = None
    mag: str | None = None
    grid: str | None = None
    wikipedia: str | None = None
    wikidata: str | None = None

    class Config:
        extra = "allow"
        frozen = True


class Geo(BaseModel):
    city: str | None = None
    geonames_city_id: str | None = None
    region: str | None = None
    country_code: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    class Config:
        extra = "allow"
        frozen = True


class AssociatedInstitution(BaseModel):
    id: str | None = None
    ror: str | None = None
    display_name: str | None = None
    country_code: str | None = None
    type: str | None = None
    relationship: str | None = None

    class Config:
        extra = "allow"
        frozen = True


class Repository(BaseModel):
    id: str | None = None
    display_name: str | None = None
    host_organization: str | None = None
    host_organization_name: str | None = None
    host_organization_lineage: list[str] = Field(default_factory=list)

    class Config:
        frozen = True


class International(BaseModel):
    display_name: dict[str, str] | None = None

    class Config:
        frozen = True


class Institution(BaseModel):
    id: str | None = None
    ror: str | None = None
    display_name: str | None = None
    country_code: str | None = None
    type: str | None = None
    type_id: str | None = None
    lineage: list[str] = Field(default_factory=list)
    homepage_url: str | None = None
    image_url: str | None = None
    image_thumbnail_url: str | None = None
    display_name_acronyms: list[str] = Field(default_factory=list)
    display_name_alternatives: list[str] = Field(default_factory=list)
    repositories: list[Repository] = Field(default_factory=list)
    works_count: int | None = None
    cited_by_count: int | None = None
    summary_stats: SummaryStats | None = None
    ids: IDs | None = None
    geo: Geo | None = None
    international: International | None = None
    associated_institutions: list[AssociatedInstitution] = Field(default_factory=list)
    counts_by_year: list[CountsByYear] = Field(default_factory=list)
    roles: list[Role] = Field(default_factory=list)
    topics: list[Topic] = Field(default_factory=list)
    topic_share: list[Topic] = Field(default_factory=list)
    x_concepts: list[XConcepts] = Field(default_factory=list)
    is_super_system: bool | None = None
    works_api_url: str | None = None
    updated_date: str | None = None
    created_date: str | None = None

    @model_validator(mode="before")
    @classmethod
    def process_international_field(cls, data) -> dict | Any:
        """
        Process the international field data
        """
        if not isinstance(data, dict):
            return data

        if data.get("international") and isinstance(data["international"], dict):
            intl = data["international"]
            if "display_name" in intl and isinstance(intl["display_name"], dict):
                intl["display_name"] = dict(sorted(intl["display_name"].items()))

        return data

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        """
        Replace None values with empty class instances for nested fields
        """
        if not isinstance(data, dict):
            return data

        if data.get("summary_stats") is None:
            data["summary_stats"] = SummaryStats()

        if data.get("ids") is None:
            data["ids"] = IDs()

        if data.get("geo") is None:
            data["geo"] = Geo()

        if data.get("international") is None:
            data["international"] = International()

        for field in [
            "repositories",
            "associated_institutions",
            "counts_by_year",
            "roles",
            "topics",
            "topic_share",
            "x_concepts",
        ]:
            if not data.get(field) or data[field] is None:
                data[field] = []

        return data

    class Config:
        frozen = True


class Message(BaseModel):
    meta: Meta | None = None
    results: list[Institution] = Field(default_factory=list)

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
