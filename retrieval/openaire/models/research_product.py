# https://graph.openaire.eu/docs/data-model/entities/research-product

from typing import Any

from pydantic import BaseModel, Field, model_validator

"""
This module contains the Pydantic models for parsing & validation OpenAIRE API responses.
The models are designed to be used with the OpenAIRE Graph API and are structured to match
the expected JSON response format for Research Products.
"""


# Sub-models for nested structures
class PidIdentifier(BaseModel):
    scheme: str | None = None
    value: str | None = None

    class Config:
        frozen = True


class PidProvenance(BaseModel):
    provenance: str | None = None
    trust: float | None = None

    class Config:
        frozen = True


class Pid(BaseModel):
    id: PidIdentifier | None = None
    provenance: PidProvenance | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("id"):
                data["id"] = PidIdentifier()
            if not data.get("provenance"):
                data["provenance"] = PidProvenance()
        return data

    class Config:
        frozen = True


class Author(BaseModel):
    fullName: str | None = None
    rank: int | None = None
    name: str | None = None
    surname: str | None = None
    pid: Pid | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict) and not data.get("pid"):
            data["pid"] = Pid()
        return data

    class Config:
        frozen = True


class BestAccessRight(BaseModel):
    code: str | None = None
    label: str | None = None
    scheme: str | None = None

    class Config:
        frozen = True


class ResultCountry(BaseModel):
    code: str | None = None
    label: str | None = None
    provenance: PidProvenance | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict) and not data.get("provenance"):
            data["provenance"] = PidProvenance()
        return data

    class Config:
        frozen = True


class CitationImpact(BaseModel):
    influence: int | None = None
    influenceClass: str | None = None
    citationCount: int | None = None
    citationClass: str | None = None
    popularity: int | None = None
    popularityClass: str | None = None
    impulse: int | None = None
    impulseClass: str | None = None

    class Config:
        frozen = True


class UsageCounts(BaseModel):
    downloads: str | None = None
    views: str | None = None

    class Config:
        frozen = True


class Indicator(BaseModel):
    citationImpact: CitationImpact | None = None
    usageCounts: UsageCounts | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("citationImpact"):
                data["citationImpact"] = CitationImpact()
            if not data.get("usageCounts"):
                data["usageCounts"] = UsageCounts()
        return data

    class Config:
        frozen = True


class AccessRight(BaseModel):
    code: str | None = None
    label: str | None = None
    openAccessRoute: str | None = None
    scheme: str | None = None

    class Config:
        frozen = True


class ArticleProcessingCharge(BaseModel):
    amount: str | None = None
    currency: str | None = None

    class Config:
        frozen = True


class ResultPid(BaseModel):
    scheme: str | None = None
    value: str | None = None

    class Config:
        frozen = True


class Instance(BaseModel):
    accessRight: AccessRight | None = None
    alternateIdentifiers: list[dict[str, str]] = Field(default_factory=list)
    articleProcessingCharge: ArticleProcessingCharge | None = None
    license: str | None = None
    pids: list[ResultPid] = Field(default_factory=list)
    publicationDate: str | None = None
    refereed: str | None = None
    type: str | None = None
    urls: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("accessRight"):
                data["accessRight"] = AccessRight()
            if not data.get("articleProcessingCharge"):
                data["articleProcessingCharge"] = ArticleProcessingCharge()
            if not data.get("pids"):
                data["pids"] = [ResultPid()]

        return data

    class Config:
        frozen = True


class Language(BaseModel):
    code: str | None = None
    label: str | None = None

    class Config:
        frozen = True


class Subject(BaseModel):
    subject: dict[str, str] | None = None
    provenance: PidProvenance | None = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("subject"):
                data["subject"] = {}
            if not data.get("provenance"):
                data["provenance"] = PidProvenance()
        return data

    class Config:
        frozen = True


# Container for Publication
class Container(BaseModel):
    edition: str | None = None
    iss: str | None = None
    issnLinking: str | None = None
    issnOnline: str | None = None
    issnPrinted: str | None = None
    name: str | None = None
    sp: str | None = None
    ep: str | None = None
    vol: str | None = None

    class Config:
        frozen = True


# GeoLocation for Data
class GeoLocation(BaseModel):
    box: str | None = None
    place: str | None = None
    point: str | None = None

    class Config:
        frozen = True


# Main ResearchProduct model
class ResearchProduct(BaseModel):
    id: str | None = None
    type: str | None = None
    originalIds: list[str] = Field(default_factory=list)
    mainTitle: str | None = None
    subTitle: str | None = None
    authors: list[Author] = Field(default_factory=list)
    bestAccessRight: BestAccessRight | None = None
    contributors: list[str] = Field(default_factory=list)
    countries: list[ResultCountry] = Field(default_factory=list)
    coverages: list[str] = Field(default_factory=list)
    dateOfCollection: str | None = None
    descriptions: list[str] = Field(default_factory=list)
    embargoEndDate: str | None = None
    indicators: Indicator | None = None
    instances: list[Instance] = Field(default_factory=list)
    language: Language | None = None
    lastUpdateTimeStamp: int | None = None
    pids: list[ResultPid] = Field(default_factory=list)
    publicationDate: str | None = None
    publisher: str | None = None
    sources: list[str] = Field(default_factory=list)
    formats: list[str] = Field(default_factory=list)
    subjects: list[Subject] = Field(default_factory=list)
    isGreen: bool | None = None
    openAccessColor: str | None = None
    isInDiamondJournal: bool | None = None
    publiclyFunded: str | None = None

    # for publications
    container: Container | None = None
    # for datasets
    size: str | None = None
    version: str | None = None
    geolocations: list[GeoLocation] = Field(default_factory=list)
    # for software
    documentationUrls: list[str] = Field(default_factory=list)
    codeRepositoryUrl: str | None = None
    programmingLanguage: str | None = None
    # for other research products
    contactPeople: list[str] = Field(default_factory=list)
    contactGroups: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> dict | Any:
        if not isinstance(data, dict):
            return data

        # Handle optional object fields
        obj_fields = {
            "bestAccessRight": BestAccessRight,
            "indicators": Indicator,
            "language": Language,
            "container": Container,
        }

        for field, classtype in obj_fields.items():
            if data.get(field) is None:
                data[field] = classtype()

        obj_list_fields = {
            "bestAccessRight": BestAccessRight,
            "indicators": Indicator,
            "language": Language,
            "authors": Author,
            "countries": ResultCountry,
            "instances": Instance,
            "pids": ResultPid,
            "subjects": Subject,
            "geolocations": GeoLocation,
        }
        for field, classtype in obj_list_fields.items():
            if not data.get(field) or data.get(field) is None or data.get(field) == []:
                data[field] = [classtype()]
        return data

    class Config:
        frozen = True


# Response wrapper classes
class Header(BaseModel):
    numfound: int
    maxscore: int | None = None
    querytime: int
    page: int
    pageSize: int | None = None
    nextCursor: str | None = None

    class Config:
        frozen = True


class Message(BaseModel):
    header: Header
    results: list[ResearchProduct]

    class Config:
        frozen = True
