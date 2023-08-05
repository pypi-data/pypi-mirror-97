from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Union

from vortexasdk.api.id import ID

IDsNames = Union[List[Union[ID, str]], str, ID]

ISODate = str


# noinspection PyPep8Naming
def to_ISODate(utc_datetime: datetime) -> str:
    return utc_datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


@dataclass(frozen=True)
class Entity:
    """Holds commonly used properties."""

    id: ID
    label: str
    layer: str


@dataclass(frozen=True)
class EntityWithProbability(Entity):
    """
    Extension of `Entity`, containing additional properties.

    - `probability` the probability of an entity occurring.
    - `source` the source of this entity, (is typically one of `['model', 'external_data']`
    """

    probability: float
    source: str


@dataclass(frozen=True)
class IDName:
    """Tuple containing `id` and `name`."""

    id: ID
    name: str


@dataclass(frozen=True)
class IDLayer:
    """Tuple containing `id` and `layer`."""

    id: ID
    layer: str


@dataclass(frozen=True)
class IDNameLayer:
    """Triple holding `id`, `name`, and `layer`."""

    id: ID
    layer: List[str]
    name: str


@dataclass(frozen=True)
class Node(ABC, IDName):
    """
    Abstract Base Class holding a node of a tree.

    # Attributes:
        ref_type: Identifies the reference type data
        leaf: Is this node a leaf of the hierarchical tree?
        parent: List of parents

    """

    ref_type: str
    leaf: bool
    parent: List[IDNameLayer]


@dataclass(frozen=True)
class Tag:
    """

    Represents a property that is associated with a period of time.

    A good example is if a vessel has acted as an FSO during a time period.

    [Tags Further Documentation](https://docs.vortexa.com/reference/intro-tags)

    """

    tag: str
    start_timestamp: Optional[ISODate] = None
    end_timestamp: Optional[ISODate] = None


@dataclass(frozen=True)
class Flag:
    """

    Represents a property that is associated with a vessel's flag.

    - `flag` key will be a Geography Entity ID.
    - `flag_country` key will be the ISO code for the country

    [Geography Entity Further Documentation](https://docs.vortexa.com/reference/intro-geography-entries)

    """

    tag: str
    flag: str
    flag_country: str


@dataclass(frozen=True)
class Scrubber:
    """

    Represents information about scrubbers fitted to a vessel.

    - `scrubber` key will be the type of scrubber.
    - `planned` key is if this scrubber has not yet been fitted but is planned.

    An empty `scrubber` List may mean the scrubber status is unknown or a vessel has none fitted.

    """

    tag: str
    scrubber: str
    planned: bool
