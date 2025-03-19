import duckdb

from models.enums import EntityType

from .authors import AuthorsIngestor
from .base import BaseIngestor
from .concepts import ConceptsIngestor
from .funders import FundersIngestor
from .institutions import InstitutionsIngestor
from .publishers import PublishersIngestor
from .sources import SourcesIngestor
from .topics import TopicsIngestor
from .works import WorksIngestor

# Registry of ingestors for each entity type
INGESTOR_REGISTRY: dict[EntityType, type[BaseIngestor]] = {
    EntityType.AUTHORS: AuthorsIngestor,
    EntityType.CONCEPTS: ConceptsIngestor,
    EntityType.WORKS: WorksIngestor,
    EntityType.INSTITUTIONS: InstitutionsIngestor,
    EntityType.SOURCES: SourcesIngestor,
    EntityType.PUBLISHERS: PublishersIngestor,
    EntityType.FUNDERS: FundersIngestor,
    EntityType.TOPICS: TopicsIngestor,
    # Add more ingestors as they are implemented
}


def get_ingestor(
    entity_type: EntityType | str, conn: duckdb.DuckDBPyConnection
) -> BaseIngestor:
    """Get the appropriate ingestor for the given entity type.

    Parameters
    ----------
    entity_type : EntityType | str
        The entity type to get an ingestor for
    conn : duckdb.DuckDBPyConnection
        The DuckDB connection to use for ingestion

    Returns
    -------
    BaseIngestor
        An ingestor for the given entity type

    Raises
    ------
    ValueError
        If no ingestor is available for the given entity type
    """
    if isinstance(entity_type, str):
        try:
            entity_type = EntityType(entity_type)
        except ValueError:
            raise ValueError(f"Unknown entity type: {entity_type}")

    if entity_type not in INGESTOR_REGISTRY:
        raise ValueError(f"No ingestor available for entity type: {entity_type}")

    return INGESTOR_REGISTRY[entity_type](conn)
