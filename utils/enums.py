"""
enums used in the project
"""

from enum import Enum


class Identifier(Enum):
    """
    Enum for different types of identifiers
    """

    DOI = "doi"
    ISBN = "isbn"
    ARXIV = "arxiv_id"
    PUBMED = "pubmed"
    PMID = "pmid"
    ORCID = "orcid"
    WIKIDATA = "wikidata"
    MAG = "mag"
    SCOPUS = "scopus_id"
    PATENT_NUMBER = "patent_number"
    PURE_ID = "pure_id"
    OPENAIRE_ID = "openaire_id"
