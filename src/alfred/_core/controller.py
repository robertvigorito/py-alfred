"""This module contains functions for interacting with the collections in the database and utilises the 
cache mechanism of redis to improve performance. The functions are decorated with the "@Cache.decorator" 
to cache the results.
"""
import os
from typing import Any, Dict, Generator, Optional, Type, Union, List as _List
from dataclasses import (
    dataclass as _dataclass,
    field as _field,
    fields as _fields,
)

# Wgid Modules
from alfred._core import almongo as _almongo
from alfred._core.cache_handler import Cache as _Cache
from alfred.structure import create_many as _create_many
from alfred.models import (
    assets as _assets,
    contexts as _contexts,
)
from attr import dataclass

# Define the services and collections mapping
services = {
    _assets.Asset: _almongo.assets,
    _contexts.Context: _almongo.contexts,
}


@_Cache.decorator
def context(
    project: str, sequence: Optional[str] = None, shot: Optional[str] = None, **kwargs: Any
) -> Optional[_contexts.Context]:
    """Creates a context entity and writes the directory structure for the shot in the mongo database.

    Args:
        project (str): The job code for th context level
        sequence (Optional[str]): The sequence code for the context level
        shot (Optional[str]): The shot code for the context level
        **kwargs: Additional kwargs to add the the context entity

    Returns:
        Optional[_contexts.Context]: The created context entity.
    """
    # Validate the sequence and shot is None or a string
    if sequence is not None and not isinstance(sequence, str):
        raise TypeError(f"sequence must be a string, not {type(sequence)}")
    if shot is not None and not isinstance(shot, str):
        raise TypeError(f"shot must be a string, not {type(shot)}")

    context_ = _contexts.Context(project=project, sequence=sequence, shot=shot, **kwargs)
    existing_context_ = find_one(query={"root": context_.root})
    if existing_context_:
        return existing_context_
    status = _almongo.contexts.insert_one(context_.asdict())
    context_._id = status.inserted_id  # pylint: disable=W0212
    _create_many([context_])

    return context_


def drop_none_keys(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    """Removes keys from a dictionary that have a value of None.

    Args:
        dictionary (Dict[str, Any]): The dictionary to remove the keys from.

    Returns:
        Dict[str, Any]: The dictionary with the keys removed.
    """
    return {key: value for key, value in dictionary.items() if value is not None}


def drop_model_keys(dictionary: Dict[str, Any], model: Type[_contexts.Context]) -> Dict[str, Any]:
    """Removes keys from a dictionary that are not in the model.

    Args:
        dictionary (Dict[str, Any]): The dictionary to remove the keys from.
        model (_contexts.Context): The model to compare the keys to.

    Returns:
        Dict[str, Any]: The dictionary with the keys removed.
    """
    model_keys = [model_field.name for model_field in _fields(model) if model_field.init]
    return {key: value for key, value in dictionary.items() if key in model_keys}


# pylint: disable=w1113
@_Cache.decorator
def find_one(
    query: Optional[Dict[str, Any]] = None, *args: Any, **kwargs: Any
) -> Union[_contexts.Context, None]:  # pylint: disable=w1113
    """Finds and returns a single context document from the "contexts" collection
    based on the given query.

    Args:
        query (Optional[Dict[str, Any]]): The query to filter the results. Defaults to None.
        *args: Any additional arguments to pass to the pymongo `find_one` method.
        **kwargs: Any additional keyword arguments to pass to the pymongo `find_one` method.

    Returns:
        Union[_contexts.Context, None]: Returns the matching context document as an instance
        of the `contexts.Context` class. If no matching document is found, returns `None`.
    """
    query = query or {}
    query = drop_none_keys(query)

    context_result = _almongo.contexts.find_one(filter=query, *args, **kwargs)
    if context_result is None:
        return None
    dropped_context_result = drop_model_keys(dictionary=context_result, model=_contexts.Context)
    context_result = _contexts.Context(**dropped_context_result)

    return context_result


# pylint: disable=w1113
@_Cache.decorator
def find(
    query: Optional[Dict[str, Any]] = None, *args: Any, **kwargs: Any
) -> Generator[_contexts.Context, None, None]:  # pylint: disable=w1113
    """Defines a function called find that takes a dictionary called query as an argument and
    returns a generator that yields instances of the "contexts.Context" class. The function is
    decorated with "@Cache.decorator" to cache the results.

    Args:
        query: A dictionary used as a filter when calling the "collection.find" method. Defaults to None.
        *args: Additional positional arguments passed to the "collection.find" method.
        **kwargs: Additional keyword arguments passed to the "collection.find" method.

    Returns:
        Generator[_contexts.Context, None, None]: A generator that yields instances of the "contexts.Context" class.
    """
    query = query or {}
    # Drop the keys that have a value of None because it will impact the query results
    query = drop_none_keys(query)
    context_results = _almongo.contexts.find(filter=query, *args, **kwargs)
    for context_result in context_results:
        # Pop the keys from the results and are not in the model keys
        dropped_context_result = drop_model_keys(dictionary=context_result, model=_contexts.Context)
        context_ = _contexts.Context(**dropped_context_result)
        yield context_


# pylint: disable=R0903
@_dataclass(slots=True, frozen=False, repr=True)
class Cave:
    """The cave class is used for bulk queries to the database

    Attributes:
        contexts (List["contexts.context"]): The list of contexts to be handled by the cave.
    """

    models: _List[Union[_contexts.Context, _assets.Asset]] = _field(default_factory=list)

    def release(self):
        """Release the data models to the database."""
        model_split = {}
        for model in self.models:
            model_service = services.get(type(model))
            model_split.setdefault(model_service, []).append(model)
        for service, models in model_split.items():
            service.insert_many([model.asdict() for model in models])
        _create_many(self.models)
        return True

    def dump(self):
        """Dump the cave to the database.

        Returns:
            bool: The status of the dump.
        """
        # Get the ids of the contexts
        model_split = {}
        for model in self.models:
            model_service = services.get(type(model))
            model_split.setdefault(model_service, []).append(model._id)  # pylint: disable=W0212
        for service, models in model_split.items():
            service.delete_many({"_id": {"$in": models}})

        return True

from alfred.models.assets import Asset

@dataclass(slots=True, frozen=True, repr=True)
class ReleaseModels:
    asset_models: _List[Asset] = _field(default_factory=list)

    def __post_init__(self):
        pass
        # Copy all the content in the content files and support files to the 
        # correct context root directory with the correct file name

        # Generate thumbnails for the assets of the default support file `*` or 
        # random selected key under the content files

        # Release the models to the database under the asset collection
    
    def release(self):
        for asset_model in self.asset_models:
            # Get the root context and construct the path to the asset
            context_model = asset_model.context
            
            asset_root_path = os.path.join(context_model.root, "assets",asset_model.fullname())
            
            print(asset_root_path)



        








