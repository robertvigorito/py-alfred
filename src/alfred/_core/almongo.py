"""The module allows you to extract the mongodb database collection for CRUD operations.
"""
import os as _os
from functools import lru_cache as _lru_cache

import dotenv as _dotenv
import pymongo as _pymongo


_dotenv.load_dotenv()


@_lru_cache(maxsize=None)
def collection(name: str) -> _pymongo.collection.Collection:
    """Returns a MongoDB collection with the specified name.

    Raises:
        pymongo.errors.ConnectionFailure: If the connection to the MongoDB server fails.

    Args:
        name (str): The name of the collection.

    Returns:
        pymongo.collection.Collection: The collection with the specified name.
    """
    username: str = _os.getenv("DB_USERNAME", "")
    password: str = _os.getenv("DB_PASSWORD", "")
    host: str = _os.getenv("DB_CLIENT_HOST", "")
    db_main_name: str = _os.getenv("DB_MAIN_NAME", "")

    wgid_mongo_client = _pymongo.MongoClient(username=username, password=password, host=host)
    wgid_database = wgid_mongo_client.get_database(name=db_main_name)
    wgid_collection = wgid_database[name]

    return wgid_collection
