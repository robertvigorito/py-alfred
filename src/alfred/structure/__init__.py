"""The location for structure files such as project folder layout and
database table configuration.
"""
from alfred.structure.project import (
    create_many,
    create_one,
    recursive_structure,
    Root,
    wgid_schema,
)

__all__ = ["wgid_schema", "create_one", "create_many", "Root", "recursive_structure"]
