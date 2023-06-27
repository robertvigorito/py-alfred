# Write module documentation here
"""Project folder schema.
"""
import logging as _logging
import os as _os

from enum import Enum as _Enum
from functools import lru_cache as _lru_cache
from pathlib import Path as _Path
from typing import Any, Dict, Optional



_logger = _logging.getLogger(__name__)


class Root(_Enum):
    """Enum for root directory structure."""

    FACILITY = "/vfx/projects"
    JOB = "{job}"
    SEQUENCE = "{sequence}"
    SHOT = "{shot}"

    ADJOINT_JOB: _Path = _Path(FACILITY) / _Path(JOB)
    ADJOINT_SEQUENCE: _Path = _Path(ADJOINT_JOB) / _Path(SEQUENCE)
    ADJOINT_SHOT: _Path = _Path(ADJOINT_SEQUENCE) / _Path(SHOT)


per_context_schema = {
    "assets": None,
    "renders": None,
    "configs": None,
}
job_schema = {
    "{job}": {
        "prod": {"reference": {}, "script": {}, "sound": {}, "storyboard": {}},
        "dailies": {},
    },
}
shot_schema = {
    "{shot}": {
        "houdini": [
            "crowds",
            "env",
            "fx",
            "light",
            "lookdev",
        ],
        "maya": ["anim", "model", "texture"],
        "nuke": [
            "comp",
            "env",
            "fx",
            "light",
            "prep",
        ],
        "substance": ["texture"],
    }
}


@_lru_cache(maxsize=None)
def wgid_schema() -> Dict[str, Any]:
    """Return the schema for the wgid project.

    Returns:
        Schema for the wgid project
    """
    # Add the per context schema to the job, sequence and shot schema
    copied_job_schema = job_schema.copy()
    copied_shot_schema = shot_schema.copy()

    copied_job_schema[Root.JOB.value].update({Root.SEQUENCE.value: per_context_schema})
    copied_job_schema[Root.JOB.value].update(per_context_schema)

    # Copy the shot schema to the sequence schema
    copied_shot_schema.update(per_context_schema)
    copied_job_schema[Root.JOB.value][Root.SEQUENCE.value].update(copied_shot_schema)

    return copied_job_schema


def recursive_structure(data: dict, path: str = ""):
    """Recursively iterate through a dictionary and yield the path of the directory structure.

    Args:
        data (dict): Dictionary to iterate through
        path (str): Path of the directory structure

    Yields:
        Path of the directory structure
    """
    for key, items in data.items():
        if not items:
            yield _os.path.join(path, key)

        elif isinstance(items, dict):
            for recursive_path in recursive_structure(items, _os.path.join(path, key)):
                yield recursive_path

        elif hasattr(items, "__iter__"):
            for item in items:
                yield _os.path.join(path, key, item)
        else:
            yield _os.path.join(path, key, str(items))


# Iterate through the schema and create the folder structure
def create_one(job: str, sequence: Optional[str] = None, shot: Optional[str] = None):
    """Create the folder structure for the project.

    Args:
        job (str): Job code for the project
        sequence (str): Sequence code for the project
        shot (str): Shot code for the project

    Returns:
        Optional[str]:      The context root.
    """
    if not shot:
        check_conditions = Root.SHOT.value
    elif not sequence:
        check_conditions = Root.SEQUENCE.value
    else:
        check_conditions = None

    for path in sorted(recursive_structure(wgid_schema())):
        if check_conditions and check_conditions in path:
            continue
        formatted_path = path.format(job=job, sequence=sequence, shot=shot)

        joined_formatted_path = _os.path.join(Root.FACILITY.value, formatted_path)
        _logger.info("Creating directory: %s", joined_formatted_path)
        _os.makedirs(joined_formatted_path, exist_ok=True)
        _logger.info("Directory created: %s", joined_formatted_path)

    return check_conditions


def create_many(contexts: list):
    """Create the folder structure for the project.

    Args:
        contexts (list): List of contexts to create the folder structure for

    Returns:
        True if successful
    """
    # Create the folder structure for the project
    for context in contexts:
        create_one(**context)
    return True
