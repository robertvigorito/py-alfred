"""This module provides a Context class  that can  be used to create and manage a context in Python.
A context is an object that holds data that can be used by various parts of a pipeline. The Context
class is designed to make it easy to create and manage a context in your Python code.
"""
import os as _os
from dataclasses import (
    asdict as _asdict,
    dataclass as _dataclass,
    field as _field,
)
from datetime import datetime as _datetime
from typing import Optional


@_dataclass(slots=True, frozen=False, repr=True)
class _Context:  # pylint: disable=R0903
    """This code is creating a class called _Context and  assigning variables to it. The
    variables are of type int, str, _datetime, and str. The _field method  is being used
    to set the default  value  for each of the variables  to a string. This is done with
    the default_factory parameter. The _Context class is used to store information related
    to a specific context.
    """    
    job: str = _field(default_factory=str)
    sequence: Optional[str] = _field(default=None)
    shot: Optional[int] = _field(default=None)
    
    # TODO: Move to base abstract class
    _id: str = _field(default_factory=str, init=False)
    root: str = _field(default_factory=str, init=False)
    created_by: str = _field(default_factory=lambda: _os.getenv("USER", "unknown"), init=False)
    created_at: _datetime.now = _field(default_factory=_datetime.now, init=False)

    def __post_init__(self):
        # TODO: Move to base abstract class
        from alfred import structure as _structure
        self.root = str(_structure.Root.ADJOINT_SHOT.value).format(job=self.job, sequence=self.sequence, shot=self.shot)
        self.validate()

    def validated(self):
        """Is the context validated in the database"""
        return self._id != ""

    # Validate the entry in the database
    def validate(self):
        """This code is creating a method called validate that is returning the _Context
        class.
        """
        from alfred._core import almongo
        copied_asdict = self.asdict().copy()
        copied_asdict.pop("_id", 0)
        db_context = almongo.contexts.find_one(filter=copied_asdict)
        # If it exists, update it else add it
        set_update = {"$set": copied_asdict}
        results = almongo.contexts.update_one(filter=copied_asdict, update=set_update, upsert=True)
        self._id = results.upserted_id or db_context["_id"]
        return self

    @property
    def shotcode(self):
        """This code is creating a method called shotcode that is returning the shotcode
        of the _Context class.
        """
        return self.shot.split("_")[1] or self.shot    
    
    def asdict(self):
        """This code is creating a method called asdict that is returning a dictionary
        of the variables that are assigned to the _Context class.
        """
        return _asdict(self)


context = _Context  # pylint: disable=C0103