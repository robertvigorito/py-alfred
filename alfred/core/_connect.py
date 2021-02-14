""" Internal connection module.
"""
import sqlite3


def connect():
    """
    Connect to the local database, if were on a build machine return
    database in memory.
    """
    __WGIT_DATABASE = "/software/config/alfred/wgid.db"
    try:
        wgit = sqlite3.connect(__WGIT_DATABASE)
    except sqlite3.OperationalError:
        wgit = sqlite3.connect(":memory")

    return wgit


cursor = connect().cursor()
