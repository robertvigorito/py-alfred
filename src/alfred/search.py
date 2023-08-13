"""This module provides functions for querying and retrieving data from the Alfred controller.

Functions:
- all_projects(): Returns a list of all projects in the Alfred controller.
- all_sequences(project: str): Returns a list of all sequences for the given project.
- all_sequences_shots(project: str, sequence: Optional[str] = None): Returns a dictionary of all shots for the given project and sequence.

Usage:
    import alfred.search as search

    # Get all projects
    projects = search.all_projects()

    # Get all sequences for a project
    sequences = search.all_sequences(project="my_project")

    # Get all shots for a project and sequence
    shots = search.all_sequences_shots(project="my_project", sequence="my_sequence")
"""
from typing import Optional
from alfred._core import controller as _controller


def all_projects():
    """Returns all projects.

    Returns:
        list[dict]: The projects.
    """
    all_projects_ = set()
    for context in _controller.find():
        all_projects_.add(context.job)
    all_projects_ = tuple(all_projects_)

    return all_projects_


def all_sequences(project: str):
    """Returns all sequences for the given project.

    Args:
        project (str): The project.

    Returns:
        list[dict]: The sequences.
    """
    all_sequences_ = set()
    for context in _controller.find(query={"job": project}):
        all_sequences_.add(context.sequence)
    all_sequences_ = tuple(all_sequences_)

    return all_sequences_


def all_sequences_shots(project: str, sequence: Optional[str] = None):
    """Returns all shots for the given project and sequence.

    Args:
        project (str): The project.
        sequence (str): The sequence.

    Returns:
    """
    query = {"job": project}
    if sequence:
        query["sequence"] = sequence

    sequence_shot_query = _controller.find(query=query, projection={"shot": 1, "sequence": 1})
    sequence_shot_structure = {}
    for context in sequence_shot_query:
        if context.shot in sequence_shot_structure.get(context.sequence, []):
            continue
        sequence_shot_structure.setdefault(context.sequence, []).append(context.shot)

    return sequence_shot_structure


find = _controller.find
find_one = _controller.find_one
