""" Alfred Search Module.
"""
import warnings
from collections import defaultdict

from alfred.core import cursor


def _details(query):
    """
    Query the `wgid` database based off the command.

    Args:
        query (str):        SQL command

    Returns:
        (dict) with the query details or empty list.
    """
    # Needs to be before execute, find the columns
    details = dict()
    cursor.execute(query)
    columns = [column[0] for column in cursor.description]

    # Create a dictionary from the data with key tuple of (id, code) ->> id is unique
    for job in cursor.fetchall():
        job_dict = dict()
        for info, column in zip(job, columns):
            job_dict[column] = info

        _id, code = job_dict.get("id"), job_dict.get("code")
        details[(_id, code)] = job_dict

    return details


def jobs(job=None):
    """
    Search the `WGIT` database for all job information or if job provided,
    then return details for the job.

    Keyword Args:
        job (str):      Job name

    Returns:
        (dict) with the information of all jobs inside the database.
    """
    query = "SELECT * FROM jobs"
    query += f" Where code='{job.upper()}';" if job else ";"

    return _details(query)


def renders():
    warnings.warn("Render query is under development...")


def scenes(job):
    """
    Search the `WGIT` database for all scene(s) information or if job provided,
    then return details for the scenes.

    Keyword Args:
        job (str):      Job name

    Returns:
        (dict) with the information of all jobs inside the database.
    """
    query = "SELECT * FROM scenes"
    query += f" Where code='{job.upper()}';" if job else ";"

    return _details(query)


def shots(job=None, scene=None, shot=None, shot_name=None):
    """
    Search the `WGIT` database for all shot information or if scene, shot provided,
    then return details for the shot.

    Args:
        job (str):          Job name

    Keyword Args:
        scene (str):        Scene name, defaults to None
        shot (str):         Shot name, defaults to None
        shot_name (str):     Full shot name, defaults to None

    Returns:
        (dict) with the information of all shot(s) inside the database.
    """
    if shot_name:
        query = f"SELECT * FROM shots WHERE name='{shot_name.upper()}'"
        deats = _details(query)
        key = list(deats.keys())[0]
        return deats.get(key)
    else:
        assert job, "job is requred when querying with out shot name!"
        query = f"SELECT * FROM shots WHERE job='{job.upper()}'"
        query += f" and scene='{str(scene)}'" if scene else ""
        query += f" and code='{str(shot)}';" if shot else ";"

    return _details(query)


def versions():
    warnings.warn("Version query is under development...")


def scenes_shots(job):
    """
    Query for all scenes with shot list.

    Args:
        job (str):      Job name

    Returns:
        (dict) scene key, with shot items
    """
    details = defaultdict(set)
    query = "SELECT scene, name FROM shots"
    query += f" Where job='{job.upper()}';" if job else ";"
    cursor.execute(query)

    for row, items in cursor.fetchall():
        details[row].add(items)

    return details
