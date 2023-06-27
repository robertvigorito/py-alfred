"""The create module allows us to create entities in the database and write the directory structure for the content for
the wgid pipeline.

The initial idea was to make the create module the idea location to create all nessary entities for the pipeline.

# TODO:
- [] Create a shot function
- [] Create context entry on shot creation
"""
from typing import Optional

from alfred import structure as _structure

def context(
    job: str, sequence: Optional[str] = None, shot: Optional[str] = None, **kwargs
):
    """Creates a shot entity and writes the directory structure for the shot in the mongo database.

    Args:
        job (str): The job code for th context level
        sequence (Optional[str]): The sequence code for the context level
        shot (Optional[str]): The shot code for the context level
        **kwargs: Additional kwargs to add the the context entity

    Returns:
        True if successful
    """
    from alfred.models import contexts

    # TODO: Merge these two functions
    _structure.create_one(job=job, sequence=sequence, shot=shot)
    created_context = contexts.context(job=job, sequence=sequence, shot=shot, **kwargs)
    created_context.validate()
    return created_context

