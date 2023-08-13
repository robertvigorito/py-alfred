"""In this module we are creating the abstract model for the alfred models. This skeleton
can be used by other models that need direct communication with the database.
"""
import os as _os
from abc import ABC, abstractmethod
from dataclasses import (
    MISSING,
    asdict as _asdict,
    field as _field,
    dataclass as _dataclass,
)
from datetime import datetime as _datetime
from typing import Any, Dict, List


@_dataclass
class AbstractDuck(ABC):
    """This is the base skeleton abstract class for the alfred models. The class holds
    the variables that are common to all the models. The class is also used to validate
    the data that is being stored in the database.
    
    Attributes:
        _id (str): The id of the asset
        comment (str): The comment of the asset
        created_at (datetime): The date and time the asset was created
        created_by (str): The user that created the asset
        metadata (Dict[str, Any]): The metadata of the asset
        root (str): The root of the asset
        status (str): The status of the asset
        tags (List[str]): The tags of the asset
    """
    _id: str = _field(default_factory=str, repr=True)
    comment: str = _field(default_factory=str, repr=False)
    metadata: Dict[str, Any] = _field(default_factory=dict, repr=False)
    status: str = _field(default_factory=str, repr=False)
    tags: List[str] = _field(default_factory=list, repr=False)

    # Attributes not called in the initiation of the class
    root: str = _field(default_factory=str, repr=False)
    created_by: str = _field(default_factory=lambda: _os.getenv("USER", "unknown"))
    created_at: _datetime = _field(default_factory=_datetime.now)

    def asdict(self):
        """This code is creating a method called asdict that is returning a dictionary
        of the variables that are assigned to the _Context class.
        """
        # Pop the id from the dictionary
        class_asdict = _asdict(self)
        class_asdict.pop("_id", None)
        return class_asdict

    def validated(self):
        """Is the context validated in the database"""
        return self._id != ""

    @abstractmethod
    def validate(self):
        """This code is creating a method called validate that is returning the _Context
        class.
        """
        pass

    @abstractmethod
    def fullname(self):
        """Return the full name of the _Context, which is composed of the job, sequence, and shot."""
        pass

