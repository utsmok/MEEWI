from enum import Enum


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


# use this to build the url:
# f"https://ris.utwente.nl/ws/oai?verb=ListRecords&set={collection}&metadataPrefix=mods"
# or metadataprefix 'oai_cerif_openaire'
