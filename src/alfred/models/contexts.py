"""This module provides a Context class  that can  be used to create and manage a context in Python.
A context is an object that holds data that can be used by various parts of a pipeline. The Context
class is designed to make it easy to create and manage a context in your Python code.
"""

from dataclasses import (
    dataclass as _dataclass,
    field as _field,
)
from datetime import datetime as _datetime


@_dataclass(slots=True, frozen=True, repr=True)
class _Context:  # pylint: disable=R0903
    """This code is creating a class called _Context and  assigning variables to it. The
    variables are of type int, str, _datetime, and str. The _field method  is being used
    to set the default  value  for each of the variables  to a string. This is done with
    the default_factory parameter. The _Context class is used to store information related
    to a specific context.
    """
    # TODO: Write validate for the data that is getting set
    id: int = _field(default_factory=str)  # pylint: disable=C0103
    job: str = _field(default_factory=str)
    sequence: str = _field(default_factory=str)
    shot: int = _field(default_factory=str)
    shotcode: str = _field(default_factory=str)

    created_at: _datetime = _field(default_factory=str)
    created_by: str = _field(default_factory=str)


context = _Context  # pylint: disable=C0103
