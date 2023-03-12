"""This module creates the asset model for the structured data stored in the pymongo
asset collection.
"""
from dataclasses import (
    dataclass as _dataclass,
    field
)
from typing import (
    List,
    Dict,
    Optional
)

from alfred.models.contexts import context


@_dataclass(slots=True, frozen=True)
class _Asset:
    id_: int
    context: context  # The facility, job, sequence, shot published level

    comment: str = field(default_factory=str)
    content_files: Dict[str: Optional] = field(default_factory=dict)  # Maybe return a file sequence object
    created_at = None
    created_by: str = field(default_factory=str)
    metadate: Dict[str: Optional] = field(default_factory=dict)
    name: str = field(default_factory=str)
    status: str = field(default_factory=str)
    support_files: Dict[str: Optional] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    version: int = field(default_factory=int)


"""
asset
  name
  context
    version 1
        content - usd,abc,exr
        support - nk,ma, hip
    version 2
        content - usd,abc,exr
        support - nk,ma, hip

"""