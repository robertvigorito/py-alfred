"""The module allows you to extract the mongodb database collection for CRUD operations.
"""
import os as _os
from functools import lru_cache as _lru_cache
from enum import Enum as _Enum

import dotenv as _dotenv
import pymongo as _pymongo


_dotenv.load_dotenv()
    

@_lru_cache(maxsize=None)
def __initiate_database():
    """Returns a MongoDB database.

    Raises:
        pymongo.errors.ConnectionFailure: If the connection to the MongoDB server fails.

    Returns:
        pymongo.database.Database: The database.
    """
    username: str = _os.getenv("DB_USERNAME", "")
    password: str = _os.getenv("DB_PASSWORD", "")
    host: str = _os.getenv("DB_CLIENT_HOST", "")
    db_main_name: str = _os.getenv("DB_MAIN_NAME", "")

    wgid_mongo_client = _pymongo.MongoClient(
        username=username, password=password, host=host
    )
    wgid_database = wgid_mongo_client.get_database(name=db_main_name)

    return wgid_database


class Collections(_Enum):
    contexts: str = "contexts"
    assets: str = "assets"
    renders: str = "renders"


contexts = __initiate_database()[Collections.contexts.value]
assets = __initiate_database()[Collections.assets.value]
renders = __initiate_database()[Collections.renders.value]
