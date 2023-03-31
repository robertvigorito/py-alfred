"""Alfred cache handler utilizing the redis framework.
"""
from dataclasses import dataclass, field
import pickle as _pickle
from typing import Any, Generator

from redis import Redis as _Redis


_redis_cache = _Redis()
CACHE_LENGTH = 10
QUERY_KEY = "query"


@dataclass(slots=True, eq=True, order=True)
class Cache:
    """A class used for caching results of a function call.

    Attributes:
        func (callable): The function to be cached.
        args (tuple): Non-keyword arguments to be passed to the function.
        kwargs (dict): Keyword arguments to be passed to the function.
        query (dict): A dictionary that stores the query and corresponding result.
    """

    func: callable = None  # noqa: E203

    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    query: dict = field(default_factory=dict)

    def __call__(self, *args, **kwargs) -> Generator[Any, Any, None] | Any:
        """The class callable method that acts as a wrapper for caching results
        of the database in redis cache.

        Keyword Args:
            *args: Non-keyworded variable arguments to unpack and pass to the wrapped function.
            **kwargs: Keyworded variable arguments to unpack and pass to the wrapped function.

        Returns:
            Either an Any object or a Generator object of Any type.
        """
        self.args, self.kwargs = args, kwargs
        self.parse_query()
        key_as_bytes = bytes(self.query)

        cached_results = _redis_cache.get(key_as_bytes)
        if cached_results:
            return _pickle.loads(cached_results)

        pickle_results = original_results = self.func(query=self.query, *args, **kwargs)

        # If the results is a generator, sort the data by expanding to a list
        if isinstance(pickle_results, Generator):
            pickle_results = list(pickle_results)

        results_as_bytes = _pickle.dumps(pickle_results)
        _redis_cache.set(key_as_bytes, results_as_bytes, ex=CACHE_LENGTH)

        return original_results

    def parse_query(self):
        """Parses the query parameter from the arguments and keyword arguments.

        Args:
            self (object): The instance of the class.

        Returns:
            bool: False if QUERY_KEY is not in kwargs, otherwise True.
        """
        # Assign the first argument to self.query if it exists
        if self.args:
            self.query = self.args.pop(0)

        # Check if QUERY_KEY exists in kwargs and use it to update self.query
        if QUERY_KEY not in self.kwargs:
            return False
        self.query = self.kwargs[QUERY_KEY]
        self.kwargs.pop(QUERY_KEY)

        return True

    @classmethod
    def decorator(cls, func) -> "Cache":
        """Instantiates a new object of the class with the given function.

        Args:
            cls: The class that the object should be instantiated from.
            func: The function that the object should be instantiated with.

        Returns:
            A new object of the given class with the specified function.
        """
        return cls(func=func)
