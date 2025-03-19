from enum import Enum


class EntityType(Enum):
    """Enum representing different OpenAlex entity types."""

    AUTHORS = "authors"
    CONCEPTS = "concepts"
    WORKS = "works"
    INSTITUTIONS = "institutions"
    SOURCES = "sources"
    PUBLISHERS = "publishers"
    FUNDERS = "funders"
    TOPICS = "topics"

    def __str__(self):
        return self.value


class TablePrefix(Enum):
    """Enum representing database table prefixes for different entities."""

    AUTHORS = "authors"
    CONCEPTS = "concepts"
    WORKS = "works"
    INSTITUTIONS = "institutions"
    SOURCES = "sources"
    PUBLISHERS = "publishers"
    FUNDERS = "funders"
    TOPICS = "topics"

    def __str__(self):
        return self.value
