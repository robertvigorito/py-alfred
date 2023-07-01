"""This module provides a Context class  that can  be used to create and manage a context in Python.
A context is an object that holds data that can be used by various parts of a pipeline. The Context
class is designed to make it easy to create and manage a context in your Python code.
"""
from dataclasses import (
    dataclass as _dataclass,
    field as _field,
)
from typing import Optional, Union

# Wgid Modules
from alfred.models.abstract_model import AbstractDuck as _AbstractDuck


@_dataclass(slots=True, frozen=False, repr=True)
class _Context(_AbstractDuck):  # pylint: disable=R0903
    """This code is creating a class called _Context and  assigning variables to it. The
    variables are of type int, str, _datetime, and str. The _field method  is being used
    to set the default  value  for each of the variables  to a string. This is done with
    the default_factory parameter. The _Context class is used to store information related
    to a specific context.
    """
    job: str = _field(default_factory=str)
    sequence: Optional[str] = _field(default=None)
    shot: Optional[str] = _field(default=None)

    def __post_init__(self):
        from alfred import structure as _structure
        self.root = str(_structure.Root.ADJOINT_SHOT.value).format(job=self.job, sequence=self.sequence, shot=self.shot)

    # Validate the entry in the database
    def validate(self):
        """This code is creating a method called validate that is returning the _Context
        class.
        """
        # TODO: Move this to the controller module and find a type solution across nosql collections
        from alfred._core import almongo
        copied_asdict = self.asdict().copy()
        copied_asdict.pop("_id", 0)
        db_context = almongo.contexts.find_one(filter=copied_asdict)
        # If it exists, update it else add it
        set_update = {"$set": copied_asdict}
        results = almongo.contexts.update_one(filter=copied_asdict, update=set_update, upsert=True)
        self._id = results.upserted_id or db_context["_id"]
        return self
    
    def fullname(self):
        """Return the full name of the _Context, which is composed of the job, sequence, and shot."""
        fullname_parts = [self.job]
        if self.sequence:
            fullname_parts.append(self.sequence)
        if self.shot:
            fullname_parts.append(self.shot)
        return '_'.join(fullname_parts)
    
    @property
    def shotcode(self):
        """This code is creating a method called shotcode that is returning the shotcode
        of the _Context class.
        """
        if isinstance(self.shot, str) and "_" in self.shot:
            return self.shot.split("_")[0]
        return self.shot


context = _Context  # pylint: disable=C0103
