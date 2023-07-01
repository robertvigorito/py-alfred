"""This module contains functions for interacting with the collections in the database and utilises the cache mechanism of 
redis to improve performance. The functions are decorated with the "@Cache.decorator" to cache the results.
"""
from typing import (
    Any,
    Dict,
    Generator,
    Optional,
    Union,
)

# Wgid Modules
from alfred._core.cache_handler import Cache
from alfred._core import almongo

def _remap_results(result: dict[str, Any]) -> dict[str, Any]:
    """Remap the id_key and pop_id_key in the given result dictionary.

    Args:
        result (dict): The dictionary containing the keys to be remapped.

    Returns:
        dict: A new dictionary with the keys remapped.
    """
    result["id"] = result.pop("_id")

    return result


@Cache.decorator
def find_one(query=None, *args, **kwargs) -> Union["contexts.Context", None]: # pylint: disable=keyword-arg-before-vararg
    """Finds and returns a single context document from the "contexts" collection
    based on the given query.

    Args:
        query (Optional[dict]): The query to filter the results. Defaults to None.
        *args: Any additional arguments to pass to the pymongo `find_one` method.
        **kwargs: Any additional keyword arguments to pass to the pymongo `find_one` method.

    Returns:
        Union[contexts.Context, None]: Returns the matching context document as an instance
        of the `contexts.Context` class. If no matching document is found, returns `None`.
    """
    query: dict = query or {}
    context_collection = collection("contexts")
    context_result: Dict[str, Any] = context_collection.find_one(filter=query, *args, **kwargs)
    if context_result is None:
        return None
    _remap_results(result=context_result)
    context: "contexts.Context" = contexts.Context(**context_result)

    return context


@Cache.decorator
def find(query: Optional[Dict[str, Any]] = None, *args: Any, **kwargs: Any) -> Generator[contexts.Context, None, None]:
    """Defines a function called find that takes a dictionary called query as an argument and
    returns a generator that yields instances of the "contexts.Context" class. The function is
    decorated with "@Cache.decorator" to cache the results.

    Args:
        query: A dictionary used as a filter when calling the "collection.find" method. Defaults to None.
        *args: Additional positional arguments passed to the "collection.find" method.
        **kwargs: Additional keyword arguments passed to the "collection.find" method.

    Returns:
        Generator[contexts.Context, None, None]: A generator that yields instances of the "contexts.Context" class.
    """
    query = query or {}

    context_results = almongo.contexts.find(filter=query, *args, **kwargs)
    for context_result in context_results:
        context = contexts.Context(**context_result)
        yield context









if __name__ == "__main__":
    # Find everthing in the contexts collection
    from pprint import pprint as pp
    pp(list(find()))