from typing import Any

from pydantic import BaseModel, Field, model_validator


class Author(BaseModel):
    id: str | None = None
    display_name: str | None = None
    orcid: str | None = None

    class Config:
        frozen = True


class Institution(BaseModel):
    id: str | None = None
    display_name: str | None = None
    ror: str | None = None
    country_code: str | None = None
    type: str | None = None
    lineage: list[str] = Field(default_factory=list)

    class Config:
        frozen = True


class Affiliation(BaseModel):
    raw_affiliation_string: str | None = None
    institution_ids: list[str] = Field(default_factory=list)

    class Config:
        frozen = True


class Authorship(BaseModel):
    author_position: str | None = None
    author: Author
    institutions: list[Institution] = Field(default_factory=list)
    countries: list[str] = Field(default_factory=list)
    is_corresponding: bool | None = None
    raw_author_name: str | None = None
    raw_affiliation_strings: list[str] = Field(default_factory=list)
    affiliations: list[Affiliation] = Field(default_factory=list)

    class Config:
        frozen = True


class Biblio(BaseModel):
    volume: str | None = None
    issue: str | None = None
    first_page: str | None = None
    last_page: str | None = None

    class Config:
        frozen = True


class Concept(BaseModel):
    id: str | None = None
    wikidata: str | None = None
    display_name: str | None = None
    level: int | None = None
    score: float | None = None

    class Config:
        frozen = True


class CitationNormalizedPercentile(BaseModel):
    value: float | None = None
    is_in_top_1_percent: bool | None = None
    is_in_top_10_percent: bool | None = None

    class Config:
        frozen = True


class Grant(BaseModel):
    funder: str | None = None
    funder_display_name: str | None = None
    award_id: str | None = None

    class Config:
        frozen = True


class HostOrganization(BaseModel):
    id: str | None = None
    display_name: str | None = None

    class Config:
        frozen = True


class SourcesLocation(BaseModel):
    url: str | None = None
    content_type: str | None = None

    class Config:
        frozen = True


class Source(BaseModel):
    id: str | None = None
    display_name: str | None = None
    issn_l: str | None = None
    issn: list[str] | None = Field(default_factory=list)
    is_oa: bool | None = None
    is_in_doaj: bool | None = None
    is_indexed_in_scopus: bool | None = None
    is_core: bool | None = None
    host_organization: str | None = None
    host_organization_name: str | None = None
    host_organization_lineage: list[str] | None = Field(default_factory=list)
    host_organization_lineage_names: list[str] | None = Field(default_factory=list)
    type: str | None = None

    class Config:
        frozen = True


class Sources(BaseModel):
    native_id: str | None = None
    id: str | None = None
    display_name: str | None = None
    locations: list[SourcesLocation] = Field(default_factory=list)
    issn_l: str | None = None
    issns: list[str] | None = Field(default_factory=list)
    is_oa: bool | None = None
    is_in_doaj: bool | None = None
    is_core: bool | None = None
    host_organization: HostOrganization | None = None
    type: str | None = None

    class Config:
        frozen = True


class Location(BaseModel):
    is_oa: bool | None = None
    landing_page_url: str | None = None
    pdf_url: str | None = None
    source: Source | None = None
    license: str | None = None
    license_id: str | None = None
    version: str | None = None
    is_accepted: bool | None = None
    is_published: bool | None = None

    class Config:
        frozen = True


class OpenAccess(BaseModel):
    is_oa: bool | None = None
    oa_status: str | None = None
    oa_url: str | None = None
    any_repository_has_fulltext: bool | None = None

    class Config:
        extra = "allow"
        frozen = True


class IDs(BaseModel):
    openalex: str | None = None
    doi: str | None = None
    mag: str | None = None
    pmid: str | None = None
    pmcid: str | None = None

    class Config:
        extra = "allow"
        frozen = True


class Mesh(BaseModel):
    descriptor_ui: str | None = None
    descriptor_name: str | None = None
    qualifier_ui: str | None = None
    qualifier_name: str | None = None
    is_major_topic: bool | None = None

    class Config:
        frozen = True


class APC(BaseModel):
    value: int | None = None
    currency: str | None = None
    value_usd: int | None = None
    provenance: str | None = None

    class Config:
        frozen = True


class SDG(BaseModel):
    id: str | None = None
    display_name: str | None = None
    score: float | None = None

    class Config:
        frozen = True


class CitedByPercentileYear(BaseModel):
    min: int | None = None
    max: int | None = None

    class Config:
        frozen = True


class Keyword(BaseModel):
    id: str | None = None
    display_name: str | None = None
    score: float | None = None

    class Config:
        frozen = True


class Topic(BaseModel):
    id: str | None = None
    display_name: str | None = None
    score: float | None = None

    class Config:
        frozen = True


class CountsByYear(BaseModel):
    year: int | None = None
    cited_by_count: int | None = None

    class Config:
        frozen = True


class Work(BaseModel):
    id: str | None = None
    doi: str | None = None
    title: str | None = None
    display_name: str | None = None
    relevance_score: float | None = None
    publication_year: int | None = None
    publication_date: str | None = None
    ids: IDs | None = None
    language: str | None = None
    primary_location: Location | None = None
    sources: list[Sources] = Field(default_factory=list)
    type: str | None = None
    type_crossref: str | None = None
    indexed_in: list[str] = Field(default_factory=list)
    open_access: OpenAccess | None = None
    authorships: list[Authorship] = Field(default_factory=list)
    institution_assertions: list[Institution] = Field(default_factory=list)
    countries_distinct_count: int | None = None
    institutions_distinct_count: int | None = None
    corresponding_author_ids: list[str] = Field(default_factory=list)
    corresponding_institution_ids: list[str] = Field(default_factory=list)
    apc_list: APC | None = None
    apc_paid: APC | None = None
    fwci: float | None = None
    is_authors_truncated: bool | None = None
    has_fulltext: bool | None = None
    fulltext_origin: str | None = None
    cited_by_count: int | None = None
    citation_normalized_percentile: CitationNormalizedPercentile | None = None
    cited_by_percentile_year: CitedByPercentileYear | None = None
    biblio: Biblio | None = None
    is_retracted: bool | None = None
    is_paratext: bool | None = None
    primary_topic: Topic | None = None
    topics: list[Topic] = Field(default_factory=list)
    keywords: list[Keyword] = Field(default_factory=list)
    concepts: list[Concept] = Field(default_factory=list)
    mesh: list[Mesh] = Field(default_factory=list)
    locations_count: int | None = None
    locations: list[Location] = Field(default_factory=list)
    best_oa_location: Location | None = None
    sustainable_development_goals: list[SDG] = Field(default_factory=list)
    grants: list[Grant] = Field(default_factory=list)
    datasets: list[str] = Field(default_factory=list)
    versions: list[str] = Field(default_factory=list)
    referenced_works_count: int | None = None
    referenced_works: list[str] = Field(default_factory=list)
    related_works: list[str] = Field(default_factory=list)
    abstract: str | None = None
    cited_by_api_url: str | None = None
    counts_by_year: list[CountsByYear] = Field(default_factory=list)
    updated_date: str | None = None
    created_date: str | None = None

    @model_validator(mode="before")
    @classmethod
    def invert_abstract(cls, data) -> dict | Any:
        """
        transforms the inverted index and stores it as the abstract
        """
        if not isinstance(data, dict):
            return data
        inv_index = data.get("abstract_inverted_index")
        if not isinstance(inv_index, dict):
            return data
        l_inv = [(w, p) for w, pos in inv_index.items() for p in pos]
        data["abstract"] = " ".join(
            map(lambda x: x[0], sorted(l_inv, key=lambda x: x[1]))
        )
        data["abstract_inverted_index"] = None
        return data

    class Config:
        frozen = True


class Meta(BaseModel):
    count: int | None = None
    db_response_time_ms: int | None = None
    page: int | None = None
    per_page: int | None = None
    next_cursor: str | None = None

    class Config:
        frozen = True


class GroupBy(BaseModel):
    key: str | None = None
    key_display_name: str | None = None
    count: int | None = None

    class Config:
        frozen = True


class GroupBys(BaseModel):
    key: str | None = None
    count: int | None = None

    class Config:
        frozen = True


class Message(BaseModel):
    meta: Meta | None = None
    results: list[Work] = Field(default_factory=list)
    group_by: list[GroupBy] = Field(default_factory=list)
    group_bys: list[GroupBys] = Field(default_factory=list)

    class Config:
        frozen = True
