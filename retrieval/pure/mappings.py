from enum import Enum

from pydantic import BaseModel

from .models.publications import Publication, parse_raw_pure_data as parse_publications


class PureEndpoint(Enum):
    """
    Enum for pure API collections
    each collection can be used with function get_pure_url to get the actual endpoint
    """

    PUBLICATIONS = "publications"
    PROJECTS = "projects"
    DATASETS = "datasets"
    PERSONS = "persons"
    ORGUNITS = "orgunits"
    PRODUCTS = "products"
    FUNDING = "funding"


ENDPOINT_TO_COLLECTION = mapping = {
    PureEndpoint.PUBLICATIONS: "openaire_cris_publications",  # maybe publications:all?
    PureEndpoint.PROJECTS: "openaire_cris_projects",
    PureEndpoint.DATASETS: "datasets:all",
    PureEndpoint.PERSONS: "openaire_cris_persons",  # maybe persons:all?
    PureEndpoint.ORGUNITS: "openaire_cris_orgunits",
    PureEndpoint.PRODUCTS: "openaire_cris_products",
    PureEndpoint.FUNDING: "openaire_cris_funding",
}

# select the metadataPrefix per endpoint that returns the most data
ENDPOINT_METADATA_PREFIX = {
    PureEndpoint.PUBLICATIONS: "mods",
    PureEndpoint.PROJECTS: "oai_cerif_openaire",
    PureEndpoint.DATASETS: "oai_cerif_openaire",
    PureEndpoint.PERSONS: "oai_cerif_openaire",
    PureEndpoint.ORGUNITS: "oai_cerif_openaire",
    PureEndpoint.PRODUCTS: "oai_cerif_openaire",
    PureEndpoint.FUNDING: "oai_cerif_openaire",
}


def parse_raw_pure_data(
    raw_data: str, endpoint: PureEndpoint, ids_stored: list[str] | None = None
) -> tuple[str, list[BaseModel]]:
    """
    function to parse the raw xml data from pure
    returns a tuple of the resumption token and a list of parsed items

    input:
    - raw_data: the raw xml data from pure
    - endpoint: the endpoint the data is from, used to select the correct parser

    """
    match endpoint:
        case PureEndpoint.PUBLICATIONS:
            return parse_publications(raw_data, ids_stored)
        case PureEndpoint.PROJECTS:
            raise NotImplementedError("Projects parsing not implemented yet")
        case PureEndpoint.DATASETS:
            raise NotImplementedError("Datasets parsing not implemented yet")
        case PureEndpoint.PERSONS:
            raise NotImplementedError("Persons parsing not implemented yet")
        case PureEndpoint.ORGUNITS:
            raise NotImplementedError("Orgunits parsing not implemented yet")
        case PureEndpoint.PRODUCTS:
            raise NotImplementedError("Products parsing not implemented yet")
        case PureEndpoint.FUNDING:
            raise NotImplementedError("Funding parsing not implemented yet")
    raise ValueError(f"Unknown endpoint: {endpoint}")


ENDPOINT_TO_MODEL = {
    PureEndpoint.PUBLICATIONS: Publication,
    PureEndpoint.PROJECTS: None,
    PureEndpoint.DATASETS: None,
    PureEndpoint.PERSONS: None,
    PureEndpoint.ORGUNITS: None,
    PureEndpoint.PRODUCTS: None,
    PureEndpoint.FUNDING: None,
}

# use this to build the url:
# f"https://ris.utwente.nl/ws/oai?verb=ListRecords&set={collection}&metadataPrefix=mods"
# or metadataprefix 'oai_cerif_openaire'
