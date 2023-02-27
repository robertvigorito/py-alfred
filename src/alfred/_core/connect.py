""" Internal connection module.
"""
import sqlite3

__WGIT_DATABASE = "/software/config/alfred/wgid.db"

try:
    wgit = sqlite3.connect(__WGIT_DATABASE)
except sqlite3.OperationalError:
    wgit = sqlite3.connect(":memory:")

cursor = wgit.cursor()

del __WGIT_DATABASE
