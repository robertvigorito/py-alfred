"""This module provides a Context class  that can  be used to create and manage a context in Python.
A context is an object that holds data that can be used by various parts of a pipeline. The Context
class is designed to make it easy to create and manage a context in your Python code.
"""
from dataclasses import (
    dataclass as _dataclass,
    field as _field,
)
from typing import Optional

# Wgid Modules
from alfred.models.abstract_model import AbstractDuck as _AbstractDuck
from alfred import structure as _structure


# TODO: Move to the structure module
def build_root(job: str, sequence: Optional[str] = None, shot: Optional[str] = None):
    """This code is creating a function called build_root that is returning the root
    of the _Context class.

    Args:
        job (str): The job name.
        sequence (Optional[str], optional): The sequence name. Defaults to None.
        shot (Optional[str], optional): The shot name. Defaults to None.

    Returns:
        str: The root of the _Context class.
    """
    root = str(_structure.Root.ADJOINT_SHOT.value).format(job=job, sequence=sequence, shot=shot)
    return root


@_dataclass(slots=True, frozen=False, repr=True)
class Context(_AbstractDuck):  # pylint: disable=R0903
    """This code is creating a class called _Context and  assigning variables to it. The
    variables are of type int, str, _datetime, and str. The _field method  is being used
    to set the default  value  for each of the variables  to a string. This is done with
    the default_factory parameter. The _Context class is used to store information related
    to a specific context.
    """

    project: str = _field(default_factory=str)
    sequence: Optional[str] = _field(default=None)
    shot: Optional[str] = _field(default=None)

    # The root is a property that is calculated based on the job, sequence, and shot
    root: str = _field(init=False, repr=False, default=build_root(job=project, sequence=sequence, shot=shot))

    # Validate the entry in the database
    def validate(self, force: bool = False):
        """This code is creating a method called validate that is returning the Context
        class.

        Args:
            force (bool, optional): Force the validation. Defaults to False.

        Returns:
            _Context: The validated _Context.
        """
        if self.validated() and not force:
            return self
        # TODO: Implement validation logic
        return self

    def fullname(self):
        """Return the full name of the _Context, which is composed of the job, sequence, and shot."""
        fullname_parts = [self.project]
        if self.sequence:
            fullname_parts.append(self.sequence)
        if self.shot:
            fullname_parts.append(self.shot)
        return "_".join(fullname_parts)

    @property
    def shotcode(self):
        """This code is creating a method called shotcode that is returning the shotcode
        of the _Context class.
        """
        if isinstance(self.shot, str) and "_" in self.shot:
            return self.shot.split("_")[0]
        return self.shot
