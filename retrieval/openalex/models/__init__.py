"""
This module contains the OpenAlex model classes.
These classes are used to parse and validate the OpenAlex API responses.
"""

from .author import Author, Message as AuthorMessage
from .domain import Domain, Message as DomainMessage
from .field import Field, Message as FieldMessage
from .funder import Funder, Message as FunderMessage
from .institution import Institution, Message as InstitutionMessage
from .publisher import Message as PublisherMessage, Publisher
from .source import Message as SourceMessage, Source
from .subfield import Message as SubfieldMessage, Subfield
from .topic import Message as TopicMessage, Topic
from .work import Message as WorkMessage, Work
