"""In this module we are creating the abstract model for the alfred models. This skeleton
can be used by other models that need direct communication with the database.
"""
from dataclasses import (
    MISSING,
    field as _field,
    dataclass as _dataclass,
)
from datetime import datetime as _datetime
from typing import Any, Dict, List


# Package imports
from alfred.models.abstract_duck import AbstractDuck as _AbstractDuck
from alfred.models.contexts import Context as _Context


@_dataclass
class AbstractAsset(_AbstractDuck):
    """Skeleton class for assets model in python alfred.

    Attributes:
        type_ (str): The type of the asset
        name (str): The name of the asset
        version (int): The version of the asset
        context (Any): The facility, job, sequence, shot published level
        content_files (Dict[str, Any]): The content files of the asset
        support_files (Dict[str, Any]): The support files of the asset
    """
    context: _Context = _field(default_factory=_Context, repr=False)
    type_: str = _field(default_factory=str)
    name: str = _field(default_factory=str)
    
    version: int = _field(default=1)

    # Content file and support files
    content_files: Dict[str, str] = _field(default_factory=dict, init=False)
    support_files: List[str] = _field(default_factory=list, init=False, repr=False)
    thumbnail: str = _field(default_factory=str, init=False, repr=False)





