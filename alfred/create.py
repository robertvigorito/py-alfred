"""Alfred create helper.
"""
import os
import re

from ._core.connect import wgit
from . import structure


_cursor = wgit.cursor()
commit = wgit.commit

SHOT_NAME_REGEX = re.compile(r"(?i)(?P<job>[a-z]+)_(?P<scene>\w+)_(?P<code>\w+)")
ROOT = "/vfx/projects"


def _create_from_config(key):
    """
    Create the table if it doesnt exist for the wgid database.

    Returns:
        True if successful, False otherwise
    """
    if not isinstance(key, str) and key in structure.database.tables:
        raise ValueError("Please ensure variable is a key of `alfred` configs...")

    columns = " ,".join([f"{key} {item}" for key, item in structure.database.tables.get(key, {}).items()])
    cmd = f"CREATE TABLE if not exists {key}s (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns});"

    return cmd


def _create_entity(entity, **kwargs):
    """
    Creates a row under the entity table, if the row exist
    update the table column from kwargs.

    Args:
        entity(str):        Table name
        **kwargs:           Reference alfred configs

    Returns:
        (str) sqlite insert command
    """
    keys, values = [], []
    code = kwargs.get("code")
    if code is None:
        raise ValueError("Cannot proceed without a unique `code` name...")

    for key, _ in structure.database.tables.get(entity, {}).items():
        value = kwargs.get(key)
        if value is None:
            continue

        keys.append(key)
        values.append(repr(value))

    insert_keys, insert_values = ", ".join(keys), ", ".join(values)
    script = f"""
        INSERT OR REPLACE INTO {entity}s (id, {insert_keys}) 
        VALUES ((SELECT id FROM {entity}s WHERE name={repr(kwargs.get("name"))}), 
                {insert_values});
        """

    return script


def job(**kwargs):
    """
    Adds a job entity under the jobs table in the `wgid` database.

    Args:
        kwargs(dict):       Reference alfred configs

    Returns:
        True if successful, False otherwise
    """
    key = "job"
    cmd = _create_from_config(key)
    cmd += _create_entity(key, **kwargs)
    # Submit SQL and commit changes
    _cursor.executescript(cmd)

    return True


def scene(**kwargs):
    """
    Adds a scene entity under the scenes table in the `wgid` database.

    Args:
        kwargs(dict):       Reference alfred configs

    Returns:
        True if successful
    """
    key = "scene"
    cmd = _create_from_config(key)
    cmd += _create_entity(key, **kwargs)
    # Submit SQL and commit changes
    _cursor.executescript(cmd)

    return True


def shot(**kwargs):
    """
    Adds a shot entity under the shots table in the `wgid` database.

    Args:
        kwargs(dict):       Reference alfred configs

    Returns:
        True if successful
    """
    key = "shot"
    cmd = _create_from_config(key)
    cmd += _create_entity(key, **kwargs)
    # Submit SQL and commit changes
    _cursor.executescript(cmd)

    return True


def shots(**kwargs):
    """
    From a dictionary that consist of key `shotname` parsed as `SHOW_SCENE_SHOT`
    update the item values, create a batch script to insert or update shot list.

    Examples:
        kwargs = {
            "MMS_001_001":
                "frame_range": "1001-1258",
                "description": "This is a demo",
            "MMS_001_010": "",
            "MMS_001_020": ""}

    Args:
        kwargs(dict):       Reference alfred configs

    Returns:
        True if successful
    """
    script = ""
    for i, (shot_name, data) in enumerate(kwargs.items()):
        match = SHOT_NAME_REGEX.match(shot_name)
        # Check if the shot table has been create
        if i == 0:
            script = _create_from_config("shot")
        # Invalid shot name
        if match is None:
            continue

        data = data if isinstance(data, dict) else {}
        data.update(match.groupdict())
        data["name"] = shot_name
        script += _create_entity("shot", **data)

    wgit.executescript(script)
    return True


def _recursive_structure(data, path=""):
    """

    Args:
        data(dict):         Data from structure.yaml

    Keyword Args:
        path(str):          Joined path

    Yields:
        (generator) String of the full folder path
    """
    for key, items in data.items():
        if not items:
            yield os.path.join(path, key)

        elif isinstance(items, dict):
            for recursive_path in _recursive_structure(items, os.path.join(path, key)):
                yield recursive_path

        elif hasattr(items, "__iter__"):
            for item in items:
                yield os.path.join(path, key, item)
        else:
            yield os.path.join(path, key, str(items))


def construct(job=None, shot_names=None):  # pylint: disable=redefined-outer-name)

    """
    Constructs the new project in the jobs directory by parsing the structure
    configs and create the folder structure.

    Args:
        job(str):               Job directory to create the shots
        shot_names(list):       List of `shot name`

    Returns:
        True if sucessful, False otherwise
    """
    for shot_name in shot_names:
        context = {"job": job, "shot": shot_name, "scene": "scrap"}
        match = SHOT_NAME_REGEX.match(shot_name)

        if any([match, job]):
            context.update(match.groupdict())

        for path in _recursive_structure(structure.folder_hierarchy, ROOT):
            path.format(**context)
            os.makedirs(name=path, exist_ok=True)

    return True
