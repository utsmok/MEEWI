from models.enums import EntityType

from .authors import AuthorsParser
from .base import BaseParser
from .concepts import ConceptsParser
from .funders import FundersParser
from .institutions import InstitutionsParser
from .publishers import PublishersParser
from .sources import SourcesParser
from .topics import TopicsParser
from .works import WorksParser

# Registry of parsers for each entity type
PARSER_REGISTRY: dict[EntityType, type[BaseParser]] = {
    EntityType.AUTHORS: AuthorsParser,
    EntityType.CONCEPTS: ConceptsParser,
    EntityType.WORKS: WorksParser,
    EntityType.INSTITUTIONS: InstitutionsParser,
    EntityType.SOURCES: SourcesParser,
    EntityType.PUBLISHERS: PublishersParser,
    EntityType.FUNDERS: FundersParser,
    EntityType.TOPICS: TopicsParser,
    # Add more parsers as they are implemented
}


def get_parser(entity_type: EntityType | str) -> BaseParser:
    """Get the appropriate parser for the given entity type.

    Parameters
    ----------
    entity_type : EntityType | str
        The entity type to get a parser for

    Returns
    -------
    BaseParser
        A parser for the given entity type

    Raises
    ------
    ValueError
        If no parser is available for the given entity type
    """
    if isinstance(entity_type, str):
        try:
            entity_type = EntityType(entity_type)
        except ValueError:
            raise ValueError(f"Unknown entity type: {entity_type}")

    if entity_type not in PARSER_REGISTRY:
        raise ValueError(f"No parser available for entity type: {entity_type}")

    return PARSER_REGISTRY[entity_type]()
