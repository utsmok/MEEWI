#https://graph.openaire.eu/docs/data-model/entities/research-product

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, model_validator

"""
This module contains the Pydantic models for parsing & validation OpenAIRE API responses.
The models are designed to be used with the OpenAIRE Graph API and are structured to match
the expected JSON response format for Research Products.
"""

# Sub-models for nested structures
class PidIdentifier(BaseModel):
    scheme: Optional[str] = None
    value: Optional[str] = None

    class Config:
        frozen = True

class PidProvenance(BaseModel):
    provenance: Optional[str] = None
    trust: Optional[float] = None

    class Config:
        frozen = True

class Pid(BaseModel):
    id: Optional[PidIdentifier] = None
    provenance: Optional[PidProvenance] = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> Dict | Any:
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
    fullName: Optional[str] = None
    rank: Optional[int] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    pid: Optional[Pid] = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> Dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict) and not data.get("pid"):
            data["pid"] = Pid()
        return data

    class Config:
        frozen = True

class BestAccessRight(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    scheme: Optional[str] = None

    class Config:
        frozen = True

class ResultCountry(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None
    provenance: Optional[PidProvenance] = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> Dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict) and not data.get("provenance"):
            data["provenance"] = PidProvenance()
        return data

    class Config:
        frozen = True

class CitationImpact(BaseModel):
    influence: Optional[int] = None
    influenceClass: Optional[str] = None
    citationCount: Optional[int] = None
    citationClass: Optional[str] = None
    popularity: Optional[int] = None
    popularityClass: Optional[str] = None
    impulse: Optional[int] = None
    impulseClass: Optional[str] = None

    class Config:
        frozen = True

class UsageCounts(BaseModel):
    downloads: Optional[str] = None
    views: Optional[str] = None

    class Config:
        frozen = True

class Indicator(BaseModel):
    citationImpact: Optional[CitationImpact] = None
    usageCounts: Optional[UsageCounts] = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> Dict | Any:
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
    code: Optional[str] = None
    label: Optional[str] = None
    openAccessRoute: Optional[str] = None
    scheme: Optional[str] = None

    class Config:
        frozen = True

class ArticleProcessingCharge(BaseModel):
    amount: Optional[str] = None
    currency: Optional[str] = None

    class Config:
        frozen = True

class ResultPid(BaseModel):
    scheme: Optional[str] = None
    value: Optional[str] = None

    class Config:
        frozen = True

class Instance(BaseModel):
    accessRight: Optional[AccessRight] = None
    alternateIdentifiers: List[Dict[str, str]] = Field(default_factory=list)
    articleProcessingCharge: Optional[ArticleProcessingCharge] = None
    license: Optional[str] = None
    pids: List[ResultPid] = Field(default_factory=list)
    publicationDate: Optional[str] = None
    refereed: Optional[str] = None
    type: Optional[str] = None
    urls: List[str] = Field(default_factory=list)

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> Dict | Any:
        if data is None:
            data = {}
        if isinstance(data, dict):
            if not data.get("accessRight"):
                data["accessRight"] = AccessRight()
            if not data.get("articleProcessingCharge"):
                data["articleProcessingCharge"] = ArticleProcessingCharge()
        return data

    class Config:
        frozen = True

class Language(BaseModel):
    code: Optional[str] = None
    label: Optional[str] = None

    class Config:
        frozen = True

class Subject(BaseModel):
    subject: Optional[Dict[str, str]] = None
    provenance: Optional[PidProvenance] = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> Dict | Any:
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
    edition: Optional[str] = None
    iss: Optional[str] = None
    issnLinking: Optional[str] = None
    issnOnline: Optional[str] = None
    issnPrinted: Optional[str] = None
    name: Optional[str] = None
    sp: Optional[str] = None
    ep: Optional[str] = None
    vol: Optional[str] = None

    class Config:
        frozen = True

# GeoLocation for Data
class GeoLocation(BaseModel):
    box: Optional[str] = None
    place: Optional[str] = None
    point: Optional[str] = None

    class Config:
        frozen = True

# Main ResearchProduct model
class ResearchProduct(BaseModel):
    id: Optional[str] = None
    type: Optional[str] = None
    originalIds: List[str] = Field(default_factory=list)
    mainTitle: Optional[str] = None
    subTitle: Optional[str] = None
    authors: List[Author] = Field(default_factory=list)
    bestAccessRight: Optional[BestAccessRight] = None
    contributors: List[str] = Field(default_factory=list)
    countries: List[ResultCountry] = Field(default_factory=list)
    coverages: List[str] = Field(default_factory=list)
    dateOfCollection: Optional[str] = None
    descriptions: List[str] = Field(default_factory=list)
    embargoEndDate: Optional[str] = None
    indicators: Optional[Indicator] = None
    instances: List[Instance] = Field(default_factory=list)
    language: Optional[Language] = None
    lastUpdateTimeStamp: Optional[int] = None
    pids: List[ResultPid] = Field(default_factory=list)
    publicationDate: Optional[str] = None
    publisher: Optional[str] = None
    sources: List[str] = Field(default_factory=list)
    formats: List[str] = Field(default_factory=list)
    subjects: List[Subject] = Field(default_factory.list)
    isGreen: Optional[bool] = None
    openAccessColor: Optional[str] = None
    isInDiamondJournal: Optional[bool] = None
    publiclyFunded: Optional[str] = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_classes(cls, data) -> Dict | Any:
        if not isinstance(data, dict):
            return data

        # Handle optional object fields
        obj_fields = {
            "bestAccessRight": BestAccessRight,
            "indicators": Indicator,
            "language": Language,
        }

        for field, classtype in obj_fields.items():
            if data.get(field) is None:
                data[field] = classtype()

        return data

    class Config:
        frozen = True

# Subtypes of ResearchProduct
class Publication(ResearchProduct):
    container: Optional[Container] = None

    @model_validator(mode="before")
    @classmethod
    def replace_none_with_empty_container(cls, data) -> Dict | Any:
        if isinstance(data, dict) and not data.get("container"):
            data["container"] = Container()
        return data

    class Config:
        frozen = True

class Data(ResearchProduct):
    size: Optional[str] = None
    version: Optional[str] = None
    geolocations: List[GeoLocation] = Field(default_factory=list)

    class Config:
        frozen = True

class Software(ResearchProduct):
    documentationUrls: List[str] = Field(default_factory.list)
    codeRepositoryUrl: Optional[str] = None
    programmingLanguage: Optional[str] = None

    class Config:
        frozen = True

class OtherResearchProduct(ResearchProduct):
    contactPeople: List[str] = Field(default_factory.list)
    contactGroups: List[str] = Field(default_factory.list)
    tools: List[str] = Field(default_factory.list)

    class Config:
        frozen = True

# Response wrapper classes
class Meta(BaseModel):
    count: Optional[int] = None
    page: Optional[int] = None
    size: Optional[int] = None

    class Config:
        frozen = True

class OpenAireResponse(BaseModel):
    meta: Optional[Meta] = None
    results: List[ResearchProduct] = Field(default_factory.list)

    @model_validator(mode="before")
    @classmethod
    def handle_meta(cls, data) -> Dict | Any:
        if isinstance(data, dict) and not data.get("meta"):
            data["meta"] = Meta()
        return data

    class Config:
        frozen = True


